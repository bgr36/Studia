import java.io.Serializable;

public class BinaryTree<T extends Comparable<T>> implements Serializable {

    public Node<T> root;
    private int RootX = 200;
    private int RootY = 10;
    private int HGap = 100;

    public BinaryTree() {
        root = null;
    }

    public void insert(T elem) {
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

    public boolean search(T elem) {
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

    public void delete(T elem) {
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

    public String drawTree() {
        StringBuilder sb = new StringBuilder();
        calculateXY(root, RootX, RootY,RootX,RootY, HGap, sb);
        return sb.toString();
    }

    private void calculateXY(Node<T> node, double x, double y,double prevx, double prevy, double hGap, StringBuilder sb) {
        if (node == null) {
            sb.append("null,");
            return;
        }

        sb.append(node.elem).append(" ").append((int)x).append(" ").append((int)y).append(" ").append((int)prevx).append(" ").append((int)prevy).append(",");
        calculateXY(node.left, x - hGap, y + 50,x,y, hGap / 2, sb);
        calculateXY(node.right, x + hGap, y + 50,x,y, hGap / 2, sb);
    }

}

