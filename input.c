int soma(int x, int y)
{
    int mult(int a)
    {
        return(2 * a);
    }
    return(x + mult(y));
}
void main()
{
    int a, b;
    a = 3;
    b = soma(a, 4);
    {
        int c, a;
        a = 2;
        c = soma(b, 2); /* Não dá erro */
        printf(a); /* Imprime 2 */
    }
    printf(b); /* Imprime 11 */
    printf(a); /* Imprime 3 */
    /*printf(c); /* da Erro */
}