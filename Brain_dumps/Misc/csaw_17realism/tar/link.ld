OUTPUT_FORMAT("elf32-i386", "elf32-i386",
          "elf32-i386")
OUTPUT_ARCH(i386)

ENTRY(_start)

SECTIONS
{
   . = 0x7C00;
   .attach : { *(.attach) }
   . = 0x8000000;
   .text : { *(.text) }
   .bss : { *(.bss) }
}

