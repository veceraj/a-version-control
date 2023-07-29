#include <stdio.h>

int main()
{
    int arr[] = {10, 20, 30, 40, 50};
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = 30;

    for (int i = 0; i < n; i++)
    {
        if (arr[i] == x)
        {
            printf("Element found at index %d\n", i);
            return 0;
        }
    }
    printf("Element not found\n");

    return 0;
}