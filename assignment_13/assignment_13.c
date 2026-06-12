#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t length;
    size_t capacity;
} StringBuffer;

StringBuffer* sb_init(size_t initial_capacity) {
    if (initial_capacity == 0) {
        initial_capacity = 16; 
    }

    StringBuffer *sb = (StringBuffer*)malloc(sizeof(StringBuffer));
    if (sb == NULL) {
        return NULL;
    }

    sb->data = (char*)malloc(initial_capacity);
    if (sb->data == NULL) {
        free(sb);
        return NULL;
    }

    sb->data[0] = '\0';
    sb->length = 0;
    sb->capacity = initial_capacity;

    return sb;
}

int sb_append(StringBuffer *sb, const char *str) {
    if (sb == NULL || str == NULL) {
        return 0;
    }

    size_t str_len = strlen(str);
    size_t needed_capacity = sb->length + str_len + 1; 
    if (needed_capacity > sb->capacity) {
        size_t new_capacity = sb->capacity * 2;
        
        while (new_capacity < needed_capacity) {
            new_capacity *= 2;
        }
        char *new_data = (char*)realloc(sb->data, new_capacity);
        if (new_data == NULL) {
            fprintf(stderr, "Memory allocation failed during resize.\n");
            return 0;
        }

        sb->data = new_data;
        sb->capacity = new_capacity;
    }

     memcpy(sb->data + sb->length, str, str_len + 1);
    sb->length += str_len;

    return 1;
}

void sb_free(StringBuffer *sb) {
    if (sb != NULL) {
        if (sb->data != NULL) {
            free(sb->data);
        }
        free(sb);          
    }
}

int main() {
    StringBuffer *sb = sb_init(10);
    if (sb == NULL) {
        printf("Failed to allocate buffer.\n");
        return 1;
    }

    printf("Initial state:\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           sb->data, sb->length, sb->capacity);

    sb_append(sb, "Hello");
    printf("After Append 1 (No resize needed):\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           sb->data, sb->length, sb->capacity);

    sb_append(sb, " World!");
    printf("After Append 2 (First resize):\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           sb->data, sb->length, sb->capacity);

    sb_append(sb, " This is an unnecessarily long string to demonstrate buffer growth.");
    printf("After Append 3 (Multiple resizes):\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           sb->data, sb->length, sb->capacity);

    sb_free(sb);
    printf("Buffer successfully freed. No memory leaks!\n");

    return 0;
}