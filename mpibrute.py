import ctypes
import ctypes.util
import hmac
import random
import sys

import numpy as np
from mpi4py import MPI

EXIT_REQUEST = 99

_libcrypt_name = ctypes.util.find_library("crypt")
_libcrypt = ctypes.CDLL(_libcrypt_name)
_libcrypt.crypt.restype = ctypes.c_char_p
_libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

def _crypt(word, salt):
    reuslt = _libcrypt.crypt(word.encode("utf-8"), salt.encode("utf-8"))
    return reuslt.decode("utf-8")

def chunk_word_list(num_ranks):
    with open("words.txt", "r") as file:
        words = [line.strip() for line in file]

    # Chunk list of words based on the number of ranks
    random.shuffle(words)
    chunks = np.array_split(words, max(num_ranks - 1, 1))
    return [chunk.tolist() for chunk in chunks]


def parse_shadow_file():
    entries = []

    with open("shadow.txt", "r") as file:
        for line in file:
            name, hash = line.strip().split(":")[:2]
            entries.append((name, hash))

    return entries


def is_matching_password(word, hash_string):
    return hmac.compare_digest(_crypt(word, hash_string), hash_string)


def main():
    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_ranks = comm.Get_size()

    if num_ranks < 2:
        print("ERROR: Must run with atlest two ranks")
        sys.exit(1)

    if rank == 0:
        print(f"Running with {num_ranks} ranks")
        word_chunks = chunk_word_list(num_ranks)
    else:
        word_chunks = None

    shadow_entries = parse_shadow_file()

    # Broadcast chunks to ranks
    rank_chunks = comm.bcast(word_chunks, root=0)

    for name, hash in shadow_entries:
        start = MPI.Wtime()

        # Each rank will process its own chunk of words
        if rank != 0:
            words = rank_chunks[rank - 1]

            # Non blocking recieve waiting for exit request
            exit_request = comm.irecv(source=MPI.ANY_SOURCE, tag=EXIT_REQUEST)

            for word in words:
                # Check if exit request has been received (password found by another rank)
                should_exit = exit_request.Test()
                if should_exit:
                    break

                if is_matching_password(word, hash):
                    # Notify worker ranks that password has been found
                    for worker_rank in range(1, num_ranks):
                        if worker_rank != rank:
                            comm.isend(None, dest=worker_rank, tag=EXIT_REQUEST)

                    end = MPI.Wtime()
                    print(f"{name}: {word} {end - start:.2f}s")
                    break

        # Wait for all ranks to finish before next iteration
        comm.Barrier()


if __name__ == "__main__":
    main()
