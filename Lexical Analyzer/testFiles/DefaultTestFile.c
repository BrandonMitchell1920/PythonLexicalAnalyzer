int main(int argc) {
    int x, y, z;
    x=0;
    y=1;
    z = sum(x,y);
    z += mult(x,y);
    return z;
}

/* Test comment */

int sum(int a, int b) {
    return a+b;
}
int mult(int a, int b) {
    return a*b;
}

/* Comment */