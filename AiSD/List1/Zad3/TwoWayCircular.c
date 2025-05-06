#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Node{
    int data;
    struct Node* next;
    struct Node* prev;
}Node;

typedef struct CircList{
    int size;
    Node* root;
}CircList;

void init(CircList* list) {
    list->size = 0;
    list->root = NULL; 
}

void insert(CircList* list,int value){

    Node* newNode = (Node*)malloc(sizeof(Node));
    if(!newNode){
        printf("Malloc failed");
        return;
    }
    newNode->data = value;

    if(list->size == 0){
        newNode->next = newNode;
        newNode->prev = newNode;
        list->root = newNode;
    } else {
        Node* last = list->root->prev;
        last->next = newNode;
        list->root->prev = newNode;
        newNode->next = list->root;
        newNode->prev = last;

    }
    list->size++;
    //printf("Inserted: %d, size %d\n",value,list->size);
}

CircList* merge(CircList* L1,CircList* L2){

    if(L1->root == NULL) return L2;
    if(L2->root == NULL) return L1;

    Node* last1 = L1->root->prev;
    Node* last2 = L2->root->prev;

    CircList* list = (CircList*)malloc(sizeof(CircList));
    
    list->root = L1->root;

    last1->next = L2->root;
    L2->root->prev = last1;

    last2->next = list->root;
    L1->root->prev = last2;

    list->size = L1->size + L2->size; 

    return list;
}

void printList(CircList* list){

    if(list->size == 0){
        printf("printList: List is empty\n");
        return;
    }

    Node* node = list->root;
    for(int i = 0;i < list->size;i++){
        printf("printList: %d\n",node->data);
        node = node->prev;
    }
    return;
}

void mergeTest(){
    CircList list1;
    init(&list1);
    insert(&list1,12);
    insert(&list1,42);
    insert(&list1,65);
    insert(&list1,55);
    insert(&list1,92);
    insert(&list1,40);
    insert(&list1,34);
    insert(&list1,83);
    insert(&list1,33);
    insert(&list1,43);


    CircList list2;
    init(&list2);
    insert(&list2,54);
    insert(&list2,22);
    insert(&list2,53);
    insert(&list2,71);
    insert(&list2,89);
    insert(&list2,56);
    insert(&list2,48);
    insert(&list2,39);
    insert(&list2,24);
    insert(&list2,77);

    CircList* list3 = merge(&list1,&list2);

    printf("List1:\n");
    printList(&list1);
    printf("List2:\n");
    printList(&list2);
    printf("List3:\n");
    printList(list3);
}

int getRandom(int min, int max){
    return min + rand() % (max - min + 1);
}

int findInList(CircList* list,int toFind,int* comp) {

    Node* node = list->root;

    if((rand() % 2) == 0){
        for(int i = 0;i < list->size;i++){
            (*comp)++;
            if(node->data == toFind){
                return 1;
            }
            node = node->next;
        }
    }else{
        for(int i = 0;i < list->size;i++){
            (*comp)++;
            if(node->data == toFind){
                return 1;
            }
            node = node->prev;
        }
    }

    return 0;

}

void firstTest(){
    
    int T[10000];
    int sum = 0;
    double avgComps;
    CircList list;
    init(&list);

    for(int i = 0;i < 10000;i++){
        T[i] = getRandom(0,100000);
        insert(&list,T[i]);
    }

    for(int i = 0;i < 1000;i++){
        int toFind = T[getRandom(0,9999)];
        findInList(&list,toFind,&sum);
    }

    avgComps = sum/1000.0;
    printf("Averag comparisons: %f\n",avgComps);
}

void secondTest(){

    int T[10000];
    int sum = 0;
    double avgComps;
    CircList list;
    init(&list);

    for(int i = 0;i < 10000;i++){
        T[i] = getRandom(0,100000);
        insert(&list,T[i]);
    }

    for(int i = 0;i < 1000;i++){
        int toFind = getRandom(0,100000);
        findInList(&list,toFind,&sum);
    }

    avgComps = sum/1000.0;
    printf("Averag comparisons: %f\n",avgComps);
}

int main(){

    srand(time(NULL));

    mergeTest();

    firstTest();

    secondTest();

    return 0;
}