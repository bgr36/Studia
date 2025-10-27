public class Node<T> {
    T elem;
    Node<T> left;
    Node<T> right;

    public Node(T Elem) {
        elem = Elem;
        left = null;
        right = null;
    }
}