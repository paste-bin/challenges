#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char stored_pass[] = "***";
char flag[] = "***";

int main()
{
    unsigned char password_len;
    puts("Enter password len :");
    scanf("%d\n", &password_len);
    
    if (password_len == 0) {
        puts("Password can't be 0 characters long");
        return 1;
    }
    
    char *pass;
    pass = malloc((int)password_len + 1);
    int i;
    for (i = 0; i < password_len; ++i) {
        pass[i] = fgetc(stdin);
    }
    
    int stored_pass_len = strlen(storemin_len	int	4	4d_pass) + 1;
    ++password_len;
    int min_len = (password_len < stored_pass_len) ? password_len : stored_pass_len;
    for (i = 0; i < min_len; ++i) {
        if (pass[i] != stored_pass[i]) {
            
            puts("Wrong pass!");
            return 1;
        }
    }
    puts(flag);
    return 0;
}