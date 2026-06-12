#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void accessElement(int *arr, int index) {
    int temp = arr[index];
}

int binarySearch(int *arr, int l, int r, int x) {
    while (l <= r) {
        int m = l+(r-l) / 2;
        if (arr[m] == x) return m;
        if (arr[m]<x) l = m+1;
        else r = m-1;
    }
    return -1;
}

int linearSearch(int *arr, int n, int x) {
    for (int i=0; i<n; i++) {
        if (arr[i] == x) return i;
    }
    return -1;
}

void bubbleSort(int *arr, int n) {
    for (int i=0; i<n - 1; i++) {
        for (int j=0; j<n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

int main() {
    int sizes[] = {1000, 5000, 10000, 20000}; 
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);

    for (int i=0; i<num_sizes; i++) {
        int n = sizes[i];
        
        int *arr = (int*)malloc(n * sizeof(int));
  
        srand(time(NULL)); 
        for (int j = 0; j < n; j++) {
            arr[j] = rand() % 100000;
        }

        clock_t start, end;
        double time_taken;
        
        printf("\nTime complexity for input size: %d\n", sizes[i]);

        start = clock();
        accessElement(arr, n-1);
        end = clock();
        double time_constant = ((double)(end - start)) / CLOCKS_PER_SEC;
        printf("Constant time O(1): %-15.6f\n", time_constant);


        start = clock();
        linearSearch(arr, n, -1); 
        end = clock();
        double time_linear = ((double)(end - start)) / CLOCKS_PER_SEC;
        printf("Linear time O(n): %-15.6f\n", time_linear);
        
        start = clock();
        binarySearch(arr, 0, n-1, -1);
        end = clock();
        double time_log = ((double)(end - start)) / CLOCKS_PER_SEC;
        printf("Logarithmic time O(nlogn): %-15.6f\n", time_log);

        start = clock();
        bubbleSort(arr, n);
        end = clock();
        double time_quadratic = ((double)(end - start)) / CLOCKS_PER_SEC;
        printf("Quadratic time O(n^2): %-15.6f\n", time_quadratic);



        free(arr);
    }
