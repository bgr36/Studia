#include <stdio.h>
#include <stdlib.h>

typedef struct Stack {
    int data;
    struct Stack* next;
} Stack;

void AddToStack(Stack** top, int item) {
    Stack* newNode = (Stack*)malloc(sizeof(Stack));
    if (!newNode) {
        printf("Malloc failed!\n");
        return;
    }
    newNode->data = item;
    newNode->next = *top;
    *top = newNode;
    printf("Added to Stack: %d\n", item);
}

int TakeFromStack(Stack** top) {
    if (*top == NULL) {
        printf("Stack is empty!\n");
        return -1;
    }
    Stack* temp = *top;
    int item = temp->data;
    *top = (*top)->next;
    free(temp);
    printf("Taken From Stack: %d\n", item);
    return item;
}

int main(){

    Stack* s = NULL;

    for(int i = 0;i < 50;i++){
        AddToStack(&s,i);
    }

    for(int i = 0;i < 50;i++){
        TakeFromStack(&s);
    }

    return 0;
}