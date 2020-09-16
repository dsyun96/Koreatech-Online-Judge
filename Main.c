# define _CRT_SECURE_NO_WARNINGS
# include <stdio.h>
# include <stdlib.h>

int Is_HN(int n)
{
    int gap1=0,gap2=0;
    if (n == 1000)
        return 0;
    if (n < 100)
        return 1;
    gap1 = n % 10 - n / 10 % 10;
    n /= 10;
    gap2 = n % 10 - n / 10 % 10;
    if (gap1 == gap2)
        return 1;
    else
        return 0;
}

int main()
{
    int n,i,cnt=0;
    scanf("%d", &n);
    for (i = 1; i < n+1; i++)
        if (Is_HN(i) == 1)
            cnt++;
    printf("%d", 0);
    return 0;
}
