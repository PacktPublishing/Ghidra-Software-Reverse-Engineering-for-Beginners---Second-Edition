#include <stdio.h>
#include <string.h>

void simple_encoder(char *input_string, char *encoded_string) {
    int val;

  __asm__ __volatile__(
        ".intel_syntax noprefix;"
        "push 1;"
        "pop rax;"
        ".att_syntax prefix;"
        : "=r" (val)
    );

    for (int i = 0; i < strlen(input_string); i++) {
        encoded_string[i] = input_string[i] + val;
    }
    encoded_string[strlen(input_string)] = '\0';
}

int main() {
    char input_string[] = "Hello, world!";
    char encoded_string[100] = "";
    
    simple_encoder(input_string, encoded_string);
    printf("Encoded string: %s\n", encoded_string);
    
    return 0;
}
