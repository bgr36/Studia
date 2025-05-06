#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    Node* front;
    Node* rear;
} Queue;

void initQ(Queue *q){
    q->front = q->rear = NULL;
}

void AddToQueue(Queue* q, int item) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        printf("Malloc failed!\n");
        return;
    }
    newNode->data = item;
    newNode->next = NULL;
    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
    printf("Added to Queue: %d\n", item);
}

int TakeFromQueue(Queue* q) {
    if (q->front == NULL) {
        printf("Queue is empty!\n");
        return -1;
    }
    Node* temp = q->front;
    int item = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) {
        q->rear = NULL;
    }
    free(temp);
    printf("Taken form Queue: %d\n", item);
    return item;
}

int main(){

    Queue q;
    initQ(&q);

    for(int i = 0;i < 50;i++){
        AddToQueue(&q,i);
    }

    for(int i = 0;i < 50;i++){
        TakeFromQueue(&q);
    }

    return 0;
}
