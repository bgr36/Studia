import java.io.Serializable;

public class BinaryTree<T extends Comparable<T>> implements Serializable {
    public Node<T> root;

    public BinaryTree() {
        root = null;
    }

    public void Insert(T elem) {
        root = insert(elem, root,null);
    }

    private Node<T> insert(T elem, Node<T> node, Node<T> parentNode) {
        if (node == null) {
            Node a = new Node<>(elem);
            System.out.println("Element :" + elem.toString());
            if(parentNode != null){
                System.out.println("Rodzic :" + parentNode.elem);
            }
            return a;
        }

        if (elem.compareTo(node.elem) < 0) {
            node.left = insert(elem, node.left,node);
        } else if (elem.compareTo(node.elem) > 0) {
            node.right = insert(elem, node.right,node);
        }

        return node;
    }

    public boolean Search(T elem) {
        return search(root, elem);
    }

    private boolean search(Node<T> node, T elem) {
        if (node == null) {
            return false;
        }

        if (elem.compareTo(node.elem) == 0) {
            return true;
        }

        if (elem.compareTo(node.elem) < 0) {
            return search(node.left, elem);
        } else {
            return search(node.right, elem);
        }
    }

    public void Delete(T elem) {
        root = delete(root, elem);
    }

    private Node<T> delete(Node<T> node, T elem) {
        if (node == null) {
            return null;
        }

        if (elem.compareTo(node.elem) < 0) {
            node.left = delete(node.left, elem);
        } else if (elem.compareTo(node.elem) > 0) {
            node.right = delete(node.right, elem);
        } else {
            if (node.left == null) {
                return node.right;
            } else if (node.right == null) {
                return node.left;
            }
            node.elem = minValue(node.right);
            node.right = delete(node.right, node.elem);
        }
        return node;
    }

    private T minValue(Node<T> node) {
        T minValue = node.elem;
        while (node.left != null) {
            minValue = node.left.elem;
            node = node.left;
        }
        return minValue;
    }

    public String Draw() {
        StringBuilder sb = new StringBuilder();
        draw(root, 1,sb);
        return sb.toString();
    }

    private void draw(Node<T> node, int depth, StringBuilder sb) {
        if (node == null) {
            return;
        }

        draw(node.right, depth + 1, sb);

        for (int i = 0; i < depth; ++i) {
            sb.append("    ");
        }

        sb.append(node.elem).append(",");

        draw(node.left, depth + 1, sb);
    }
}
