#!/usr/bin/env python3
import argparse
import sys
import socket
from library import CTFDict, Colors, generate_challenge_and_answer, ASCII_ART
from loguru import logger
from threading import Thread
from time import sleep


class ClientThread(Thread):
    def __init__(self, client_socket: socket.socket, ip: str, port: int):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = ip
        self.client_port = port

    def run(self):
        self.client_socket.sendall(ASCII_ART.encode())
        solver_ctr = 0
        while True:
            try:
                challenge, answer = generate_challenge_and_answer()
                self.client_socket.sendall((f"ROUND {solver_ctr}\n" + challenge).encode())
                self.client_socket.sendall(bytes(">>> ", "utf-8"))
                cli_answer = self.client_socket.recv(1024).decode().strip()
                if cli_answer == answer:
                    solver_ctr += 1
                    if solver_ctr == 100:
                        self.client_socket.sendall((CTFDict.WON + CTFDict.FLAG).encode())
                        self.closeConn()
                        return
                else:
                    self.client_socket.sendall(CTFDict.WRONG_ANSWER.encode())
                    self.closeConn()
                    return
            except (BrokenPipeError, ConnectionResetError):
                self.closeConn()
                return

    def closeConn(self):
        self.client_socket.close()
        logger.info(
            f"{Colors.FAIL}[-] Client {self.client_ip}:{self.client_port} disconnected {Colors.ENDC}"
        )


class Server:
    def __init__(self, address: str, port: int):
        self.initConn(address, port)

    @classmethod
    def initConn(self, address: str, port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except Exception:
            logger.error(
                "Could not bind address to port, use a different port or try again later"
            )
            sys.exit()
        while True:
            try:
                (client_socket, (ip, port)) = server_socket.accept()
                logger.info(
                    f"{Colors.OKGREEN}[+] Connection established from {ip} at port {port} {Colors.ENDC}"
                )
                client_thread = ClientThread(client_socket, ip, port)
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                logger.warning(
                    f"\n{Colors.WARNING}We are shutting down the server {Colors.ENDC}"
                )
                sleep(1)
                break
            except Exception as e:
                logger.error(f"{Colors.FAIL}Error occured {e} {Colors.ENDC}")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", metavar="", type=int, help="specify server's port", default=2802
    )
    parser.add_argument(
        "-a",
        "--address",
        metavar="",
        type=str,
        help="specify server's address",
        default="127.0.0.1",
    )
    group = parser.add_mutually_exclusive_group()
    args = parser.parse_args()
    try:
        logger.info(f"Listening at {args.port}")
        server = Server(args.address, args.port)
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()
