# ifndef LOCATE_PTR_H
# define LOCATE_PTR_H
/*
The header file contains two separate functions (each serving a distinct purpose):

One function retrieves the size of the memory allocation corresponding to the provided pointer.

The other function returns the index associated with the pointer.
*/

/*
Since these functions rely on debugging utilities from LLVM's AddressSanitizer, the code must be compiled with Clang, and the following flags are required during compilation:

-g -fsanitize=address
*/
#include <sanitizer/asan_interface.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

size_t mem_size(char *s){
    char name[100];
    size_t name_size = 100;
    void *region_address = NULL;
    size_t region_size = 0;

    const char* alloc_info = __asan_locate_address(s, name, name_size, &region_address, &region_size);
    // printf("alloc_info: %s\n", alloc_info);  //buffer heap ...
    // printf("name: %s\n", name);
    // printf("region address: %p\n", region_address);
    // printf("region size: %zu\n", region_size);
    // printf("reach address: %p\n", s);
    // printf("reach index: %ld\n", s - (char *)region_address);
    if (alloc_info) {
        return region_size;
    }
    assert (0 && "Failed to locate buffer");
    return 0;
}

int ptr_index(char *s){
    char name[100];
    size_t name_size = 100;
    void *region_address = NULL;
    size_t region_size = 0;

    const char* alloc_info = __asan_locate_address(s, name, name_size, &region_address, &region_size);
    if (alloc_info) {
        return s - (char *)region_address;
    }
    assert (0 && "Failed to locate buffer");
    return 0;
}
