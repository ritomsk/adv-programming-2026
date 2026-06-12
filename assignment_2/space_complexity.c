#include <stdio.h>
#include <stdlib.h>

void constant_operation(long n) {
    long memory_bytes = 0;
    printf("Constant(O(1))  - N: %-6ld | Memory: %-12ld bytes\n", n, memory_bytes);
}

void linear_operation(long n) {
    long memory_bytes = n*sizeof(int);
    int *arr = (int*)malloc(memory_bytes);
    
    if (arr != NULL) {
        for (long i = 0; i < n; i++) {
            arr[i] = i;
        }
        printf("Linear(O(N))  - N: %-6ld | Memory: %-12ld bytes\n", n, memory_bytes);
        free(arr);
    } else {
        printf("Linear(O(N))  - N: %-6ld | Memory Allocation Failed\n", n);
    }
}

void quadratic_operation(long n) {
    long memory_bytes = n * n * sizeof(int);
    int *arr = (int*)malloc(memory_bytes);
    
    if (arr != NULL) {
        for (long i = 0; i<n; i++) {
            for (long j = 0; j<n; j++) {
                arr[i * n+j] = i+j;
            }
        }
        printf("Quadratic(O(N^2)) - N: %-6ld | Memory: %-12ld bytes\n", n, memory_bytes);
        free(arr);
    } else {
        printf("Quadratic(O(N^2)) - N: %-6ld | Memory allocation failed\n", n);
    }
}

int main() {
    long inputs[] = {10, 100, 1000, 5000};
    int steps = sizeof(inputs)/sizeof(inputs[0]);

    for (int i = 0; i<steps; i++) {
        constant_operation(inputs[i]);
        linear_operation(inputs[i]);
        quadratic_operation(inputs[i]);
        printf("------------------\n");
    }

    return 0;
}

