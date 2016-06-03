/*
GOAL: Create a simple version control (svc) program called "svc".

DETAILS:

We have a text file that needs version control i.e., ability to revert back
to any previous version.  
- The text that is composed of one or more lines.
- Each line has a maximum character width of 10 characters (including newline).
- The total number of lines is 20.

The following operations are permitted:
1. Appending a new line at the end of the file.
2. Deleting any existing line.

Only one of the above operations can be done at a given time i.e., the user
can either append a line -or- delete a line. After each operation, the file
is commited using the svc. 

 When a commit is made, only one change is recorded.
 
 A file 'revert1' stores the changes.
 The format of the changes stored in 'revert1' are:
 		v:N  -Version N (0 based)
 		+:S  -Append line S
 	OR	-:n  -Delete line n (0 based)
 		e:e  -End of version N description
 
 * */
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINES 20
#define MAX_SIZE 12

int check(char arg[])
{
	int i = 0, type = 1;
	for(i=0; arg[i]!='\0'; i++) 
	{
		if(arg[i] >= '0' && arg[i] <= '9')
			type = 0;
		else
		{
			type = 1;
			break;
		}
	}
	return type;
}
//Function which construct nth version file
//in case of new file commit this function gives most recent version file
int getFile(int version, char file[MAX_LINES][MAX_SIZE],int getMostRecent, int * mostRecentVersionNo)
{
	FILE * revertFile = NULL;
	char * line = NULL;
	ssize_t read = 0;
	size_t len = 0;

	int v = 0;
	int file_i = 0;
	int i;
	int exitAfterEnd = 0;
	int exitLoop = 0;

	char info;
	char data[MAX_SIZE];

	revertFile = fopen("revert1", "r");
	if(revertFile == NULL) 
	{
		return 0;
	}

	//clear file
	for(i=0; i<MAX_LINES; i++)
		file[i][0] = '\0';

	exitLoop = 0;
	while( (read = getline(&line, &len, revertFile)) != -1) 
	{

		line[strlen(line) - 1] = '\0';

		info = line[0];
		strcpy(data, line+2);

		switch(info)
		{
			case '+':
			{
				strcpy(file[file_i], data);
				file_i++;
				break;
			}
			case '-':
			{
				int lineNo=atoi(data);				
				for(i = lineNo; i<file_i; i++)
					strcpy(file[i], file[i+1]);
				file_i--;
				break;
			}
			case 'v':
			{
				v=atoi(data);				
				if(v == version)
					exitAfterEnd = 1;
				break;
			}
			case 'e':
			{
				if(exitAfterEnd == 1 && getMostRecent == 0)
				{
					exitLoop = 1;
					break;
				}
				break;
			}
		}

		if(exitLoop)
			break;
	}

	free(line);
	fclose(revertFile);
	*mostRecentVersionNo = v;
	return file_i;
}

//Function to compare the latest file with most recent version file
//and update revert1 file if any changes found 
int comparePrev(char prevfile[MAX_LINES][MAX_SIZE], int prevfileVersion, int lines, char filename[])
{
	FILE * currentFile = NULL;
	FILE * revertFile = NULL;

	int prevfileLineNo = 0;

	char * line = NULL;
	size_t len = 0;
	ssize_t read = 0;

	char change[MAX_SIZE] = "\0";
	int changesFound = 0;

	currentFile = fopen(filename, "r");
	if(currentFile == NULL) 				//Executes at first commit means revert1 file does not exist
	{
		printf("The file %s does not exist.\n", filename);
		exit(0);
	}

	revertFile = fopen("revert1", "a");			

	while( (read = getline(&line, &len, currentFile)) != -1 )
	{
		line[strlen(line) - 1] = '\0';
		if(prevfileLineNo < lines) 
		{
			if(strcmp(prevfile[prevfileLineNo], line) != 0) 
			{
				sprintf(change, "-:%d\n", prevfileLineNo);
				break;
			}
		}
		else 
		{
			sprintf(change, "+:%s\n", line);
		}
		prevfileLineNo++;
	}

	if(prevfileLineNo < lines) 
	{
		sprintf(change, "-:%d\n", prevfileLineNo);
	}

	//stores new version entry in revert1
	if(strlen(change) > 0)
	{
		fprintf(revertFile, "v:%d\n", prevfileVersion + 1);
		printf("Change found as : %s\n",change);
		fprintf(revertFile, "%s", change);
		fprintf(revertFile, "e:e\n");
		changesFound = 1;
	}

	fclose(revertFile);
	fclose(currentFile);

	return changesFound;
}

int main(int argc, char * argv[])
{
	int argType;
	char file[MAX_LINES][MAX_SIZE];
	int mostRecentVersionNo = -1;

	if (argc <= 1)
	{
		printf("Usage:\n");
		printf("%-20s %-40s\n", "svc FILENAME", "commit file");
		printf("%-20s %-40s\n", "svc N" , "display Nth version of the file");
		printf("svc will track the versions of one file for you.\n");
		exit(0);
	}

	argType = check(argv[1]);

	if(argType == 0)		// Argument type is version number 
	{
		// Show Nth version
		int version=atoi(argv[1]);		
		int lines = getFile(version, file, 0, &mostRecentVersionNo);
		int i;
		printf("-------Version %d-------\n",version);
		for(i=0; i<lines; i++)
			printf("%s\n",file[i]);
	}
	else				//Argument type is filename
	{
		// Save current version
		int lines = getFile(0, file, 1, &mostRecentVersionNo);
		int changes = comparePrev(file, mostRecentVersionNo, lines, argv[1]);
		if(changes) printf("File committed.\n");
		else printf("The file has already been committed.\n");
	}


	return 0;

}
