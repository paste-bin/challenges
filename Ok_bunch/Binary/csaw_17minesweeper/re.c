re.c

	size_t
	delink(int a1, node *a2) {
	struct node *v2;  // ST1C_4@1

	v2 = a2->prev;
	a2->prev->next = a2->next;
	a2->next->prev = v2;
	return fwrite("delinked!", 1u, 9u, stderr);
}
