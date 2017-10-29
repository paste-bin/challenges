#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <signal.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>

static long forbidden_syscalls[] = {
  // yeah, not really exhaustive or sensible, but enough for demo purposes
  SYS_open, SYS_openat, SYS_creat
};
#define forbidden_syscalls_len ((sizeof(forbidden_syscalls)/sizeof(forbidden_syscalls[0])))

int main(void) {
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  assert(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == 0);

  struct sock_filter instrs[forbidden_syscalls_len+5];
  #define NUM_INSTRS (sizeof(instrs) / sizeof(instrs[0]))
  #define FAIL_IDX (NUM_INSTRS-1)
  #define ACCEPT_IDX (NUM_INSTRS-2)
  instrs[0] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch));
  unsigned int my_arch =
      #ifdef __x86_64__
        AUDIT_ARCH_X86_64
      #else
        #error unknown architecture
      #endif
      ;
  instrs[1] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, my_arch, 0, FAIL_IDX-(1+1));
  instrs[2] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr));
  for (int i=0; i<forbidden_syscalls_len; i++) {
    instrs[i+3] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, forbidden_syscalls[i], FAIL_IDX-(i+3+1), 0);
  }
  instrs[ACCEPT_IDX] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW);
  instrs[FAIL_IDX] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | 0x1234);
  struct sock_fprog fprog = {.len = NUM_INSTRS, .filter = instrs};

  // for debugging
  FILE *f = fopen("filter.dbg", "w");
  fwrite(fprog.filter, sizeof(instrs), 1, f);
  fclose(f);

  assert(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &fprog, 0, 0) == 0);

  // first try to open the file directly, which should fail...
  int fd = syscall(SYS_open, (unsigned long)"/etc/passwd", O_RDONLY);
  printf("open() returned -0x%x\n", -fd);

  // and now try it with x32
  int r = syscall(SYS_open | 0x40000000, (unsigned long)"/etc/passwd", O_RDONLY);
  printf("x32 open return value: 0x%x\n", r);
  char buf[30];
  ssize_t n = read(r, buf, sizeof(buf));
  if (n > 0) write(1, buf, n);
  printf("\n");
  return 0;
}
