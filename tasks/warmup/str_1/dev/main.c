// gcc -m32 main.c -o str_1

#include <stdio.h>
#include <string.h>


unsigned char* flg = "ptctf{strings_go_brbrbrbrbrbrbr}";

int main(int argc, char** argv)
{
    unsigned char buff[33];
    printf("Enter flag: ");
    fgets(buff, 33, stdin);

    if (strncmp(buff, flg, 33)) {
        puts("[-] Flag incorrect.");
    } else {
        puts("[+] Flag correct.");
    }
    return 0;
}  