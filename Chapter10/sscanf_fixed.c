#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {
	if (argc < 2)
	{
		printf("ERROR: Expected commandline args");
		return -1;
	}
	char name[20];
	int age = atoi(argv[2]); 
	int return_value = sscanf(argv[1], "%s %i", name, &age);
	if(return_value == 2){
		printf("I'm %s.\n", name);
		printf("I'm %i years old.", age);
	}else if(return_value == -1){
		printf("ERROR: Unable to read the input data.\n");
	}else{
		printf("ERROR: 2 values expected, %d given.\n", return_value);
	}
	return 0;
}
