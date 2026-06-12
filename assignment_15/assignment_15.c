#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 4
#define NUM_INCREMENTS 1000000

long long counter_race = 0;
long long counter_mutex = 0;

pthread_mutex_t lock;

void* increment_without_mutex(void* arg) {
    for (int i = 0; i < NUM_INCREMENTS; i++) {
        counter_race++; 
    }
    return NULL;
}


void* increment_with_mutex(void* arg) {
    for (int i = 0; i < NUM_INCREMENTS; i++) {
        pthread_mutex_lock(&lock);
        counter_mutex++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    long long expected_total = (long long)NUM_THREADS * NUM_INCREMENTS;

    printf("Expected Final Counter Value: %lld\n\n", expected_total);

    printf("--- Running WITHOUT Mutex ---\n");
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, increment_without_mutex, NULL);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("Final Counter (Race Condition): %lld\n", counter_race);
    printf("Lost Updates: %lld\n\n", expected_total - counter_race);

    printf("--- Running WITH Mutex ---\n");
    
    if (pthread_mutex_init(&lock, NULL) != 0) {
        printf("Mutex initialization failed.\n");
        return 1;
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, increment_with_mutex, NULL);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL); 
    }

    printf("Final Counter (Mutex Protected): %lld\n", counter_mutex);
    printf("Lost Updates: %lld\n", expected_total - counter_mutex);

    pthread_mutex_destroy(&lock);

    return 0;
}

// Why does the Race Condition occur?
// Even though counter++ looks like a single instruction in C,
// the CPU actually executes it in three separate steps at the machine level:

// READ: Read the current value of counter from RAM into a CPU register.
// MODIFY: Add 1 to the value in the register.
// WRITE: Write the new value from the register back to RAM.

// Because these steps are not atomic (indivisible), thread execution can overlap.
// Imagine counter is currently 10:

// Thread A reads 10.
// Thread B reads 10 before Thread A has a chance to write back its result.
// Thread A adds 1 and writes 11 back to RAM.
// Thread B adds 1 (to its stored 10) and also writes 11 back to RAM.

// Even though two threads did work, the counter only went up by 1 instead of 2.
//We call this a "lost update". Over millions of iterations, you lose a massive chunk of your increments.

// How does the Mutex solve it?
// A Mutex (short for Mutual Exclusion) acts like a single physical key to a locked room (the critical section).
// When a thread reaches pthread_mutex_lock(), it grabs the key. If another thread arrives,
//it sees the key is missing and is forced to "go to sleep" (block) at the door.
//It cannot proceed to the counter++ line until the first thread calls pthread_mutex_unlock(), returning the key.

// This forces the Read-Modify-Write cycle to happen sequentially, ensuring no overlaps and zero lost updates.