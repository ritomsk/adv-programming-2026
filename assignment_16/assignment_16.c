#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5
#define NUM_PRODUCERS 2
#define NUM_CONSUMERS 2
#define ITEMS_TO_PRODUCE 6
int buffer[BUFFER_SIZE];
int in = 0;  
int out = 0; 

sem_t empty_slots; 
sem_t full_slots; 
pthread_mutex_t mutex;

void* producer(void* arg) {
    int id = *((int*)arg);
    
    for (int i = 0; i < ITEMS_TO_PRODUCE; i++) {
        int item = (id * 100) + i;
        
        sem_wait(&empty_slots);
        
        pthread_mutex_lock(&mutex);
        
        buffer[in] = item;
        printf("[Producer %d] Produced item %d at index %d\n", id, item, in);
        in = (in + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        
        sem_post(&full_slots);
        
        usleep(100000); 
    }
    return NULL;
}

void* consumer(void* arg) {
    int id = *((int*)arg);
    
    for (int i = 0; i < ITEMS_TO_PRODUCE; i++) {
        sem_wait(&full_slots);
        
        pthread_mutex_lock(&mutex);
        
        int item = buffer[out];
        printf("    [Consumer %d] Consumed item %d from index %d\n", id, item, out);
        out = (out + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        
        sem_post(&empty_slots);
        
        usleep(150000); 
    }
    return NULL;
}

int main() {
    pthread_t producers[NUM_PRODUCERS];
    pthread_t consumers[NUM_CONSUMERS];
    int thread_ids[NUM_PRODUCERS > NUM_CONSUMERS ? NUM_PRODUCERS : NUM_CONSUMERS];

    sem_init(&empty_slots, 0, BUFFER_SIZE); 
    sem_init(&full_slots, 0, 0);
    pthread_mutex_init(&mutex, NULL);

    printf("Starting Producer-Consumer Simulation...\n\n");

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&producers[i], NULL, producer, &thread_ids[i]);
    }
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_create(&consumers[i], NULL, consumer, &thread_ids[i]);
    }

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pthread_join(producers[i], NULL);
    }
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_join(consumers[i], NULL);
    }

    sem_destroy(&empty_slots);
    sem_destroy(&full_slots);
    pthread_mutex_destroy(&mutex);

    printf("\nSimulation Complete.\n");
    return 0;
}

// Explanation: How Synchronization Prevents Inconsistencies?
// If multiple threads accessed the buffer array at the exact same
// time without protection, they would overwrite each other's data
// (Data Race) or read "garbage" memory that hasn't been written yet.
// We prevent this using two layers of protection:

// 1. The Mutex (Mutual Exclusion) = Prevents Race Conditions
// The pthread_mutex_t acts as a lock on the buffer array itself.
// When a Producer is actively writing a number into the array,
// the Mutex ensures that no other Producer can write, and no Consumer can read,
// until the writing is finished. It ensures Atomicity in the critical section.

// 2. The Semaphores = Prevents Overflows & Underflows
// A Semaphore acts like an internal counter.

// empty_slots (Starts at 5): When a Producer wants to add an item,
// it calls sem_wait(&empty_slots). This decreases the counter to 4.
// If the buffer gets totally full, the counter hits 0.
// If a Producer tries to sem_wait on a 0, the operating system puts
// that Producer to sleep. It stays "Blocked" until a Consumer removes
// an item and calls sem_post(&empty_slots).

// full_slots (Starts at 0): This works the exact opposite way.
// If the buffer is completely empty, full_slots is 0.
// A Consumer trying to read will sem_wait and instantly be put
// to sleep because there is nothing to read. It wakes up the moment
// a Producer adds an item and calls sem_post(&full_slots).