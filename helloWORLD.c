#include <conio.h>
#include <stdio.h>
#include <windows.h>

int main(void)
{   // python file PATH read
    FILE *pFile = fopen("codes/Python_PATH.txt", "r");

    // if can not read python file PATH
    if(pFile == NULL)
    {   printf("Can't find 'Python_PATH.txt' file.\nPress any key to terminate...");
        getch();
        return 1;
    }
    // store python file path
    char codeFile_PATH[1000] = {"python codes/"};
    fscanf(pFile, "%s\n", &codeFile_PATH[13]);
    printf("Execute '%s'\n", codeFile_PATH);

    // execute python
    system(codeFile_PATH);
    printf("Press any key to terminate...");

    // wait user press any key
    getch();

    return 0;
}
