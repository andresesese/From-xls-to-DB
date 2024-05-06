#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

// Funzione per verificare se una libreria Python è installata
int isLibraryInstalled(const char *library) {
    char command[100];
    sprintf(command, "python -c \"import %s\"", library);
    return system(command) == 0;
}

// Funzione per installare una libreria Python se non è già installata
void installLibrary(const char *library) {
    char command[100];
    sprintf(command, "pip install %s", library);
    system(command);
}

// Funzione per verificare se un file termina con .xls
int endsWithXls(const char *filename) {
    size_t len = strlen(filename);
    return len >= 4 && strcmp(filename + len - 4, ".xls") == 0;
}

// Funzione per verificare se un file esiste
int fileExists(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file != NULL) {
        fclose(file);
        return 1;
    }
    return 0;
}

int main() {
    char files[10][100];
    int numFiles = 0;

    // Verifica e installa le librerie necessarie
    if (!isLibraryInstalled("xlrd")) {
        printf("Libreria xlrd non installata. Installando...\n");
        installLibrary("xlrd");
    }
    if (!isLibraryInstalled("openpyxl")) {
        printf("Libreria openpyxl non installata. Installando...\n");
        installLibrary("openpyxl");
    }

    // Input dei file xls
    printf("Inserisci i nomi dei file xls da analizzare (max 10, 'fine' per terminare):\n");
    while (numFiles < 10) {
        char filename[100];
        printf("File %d: ", numFiles + 1);
        scanf("%s", filename);

        if (strcmp(filename, "fine") == 0) {
            break;
        }

        if (!endsWithXls(filename)) {
            printf("Il file deve terminare con .xls\n");
            continue;
        }

        if (!fileExists(filename)) {
            printf("Il file %s non esiste nella cartella.\n", filename);
            continue;
        }

        strcpy(files[numFiles], filename);
        numFiles++;
    }

    // Costruzione del comando per eseguire il programma Python
    char command[1000] = "python programma.py";
    for (int i = 0; i < numFiles; i++) {
        strcat(command, " ");
        strcat(command, files[i]);
    }

    // Esecuzione del programma Python con i file come argomenti
    printf("Esecuzione del programma Python...\n");
    system(command);
    system("pause");
    return 0;
}
