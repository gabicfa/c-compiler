void main()
{
    int x, y, x_2, y_2, z, z_2, w, b;
    x = 3;
    y = 2;
    x_2 = scanf();
    y_2 = 5;

    {
        z = x + y;
        z_2 = x_2 + y_2;
        printf(z);
        printf(z_2);
        printf(x - -y);
    }
    
    if(z < z_2){
        printf(z);
    }
    else{
        x=1;
        y=2;
        if(x>0 && y >0){
            printf(x);
            printf(y);
        }
    }

    w = (x+y)/z_2;
    printf(    /* bla */ w /* bla */);
    /*bla bla
    bla
    bla */

    printf(  w+x);
    b = w + x;
    printf(b + w + z);
    while(b > 0){
        b=scanf();
    }
}