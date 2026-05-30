import random
import sys
import logging
from pathlib import Path

import bcrypt
import nltk
import numpy as np
from mpi4py import MPI

EXIT_REQUEST = 99

log_path = Path("~/giboneyn/mpibrute.log").expanduser()

log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(log_path),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def chunk_word_list(num_ranks):
    words = [word for word in nltk.corpus.words.words() if 6 <= len(word) <= 10]
    random.shuffle(words)

    # Chunk list of words based on the number of ranks
    chunks = np.array_split(words, max(num_ranks - 1, 1))
    return [chunk.tolist() for chunk in chunks]


def parse_shadow_file():
    entries = []

    with open("shadow.txt", "r") as file:
        for line in file:
            name, hash = line.strip().split(":")[:2]
            entries.append((name, hash))

    return entries


def is_matching_password(word, hash):
    hash_bytes = hash.encode("utf-8")
    word_bytes = word.encode("utf-8")
    return bcrypt.checkpw(word_bytes, hash_bytes)


def main():
    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_ranks = comm.Get_size()

    if num_ranks < 2:
        logging.error("ERROR: Must run with atlest two ranks")
        sys.exit(1)

    if rank == 0:
        logging.info(f"Running with {num_ranks} ranks")
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
                    logging.info(f"{name}: {word} {end - start:.2f}s")
                    break

        # Wait for all ranks to finish before next iteration
        comm.Barrier()


if __name__ == "__main__":
    main()
