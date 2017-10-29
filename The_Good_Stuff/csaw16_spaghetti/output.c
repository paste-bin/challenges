#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <pthread.h>
int output(char *format, ...);
int main(int argc, char *argv[]){
	
	output(argv[1]);

	return 0;
}
int output(char *format, ...)
{
  unsigned long v1; // ax@1
  va_list va; // [sp+24h] [bp+Ch]@1

  va_start(va, format);
  v1 = (unsigned long)pthread_self();
  printf("%s %04x ", "MOMS_SPAGHETTI", v1);
  return vprintf(format, va);
}