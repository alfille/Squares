#include <stdio.h>

// Program to find best sum of squares for all integers

#define MAX_N 100 // max integer (squared)
#define MAX_M MAX_N // max covering square

#define MAX_NN (MAX_N * MAX_N)
#define MAX_MM (MAX_M * MAX_M)

int SQ[MAX_MM] ;

void SetupSQ( void )
{
    int i;
    for ( i=0 ; i<MAX_MM ; ++i ) {
        SQ[i] = (i+1)*(i+1)*(i+1) ;
        if ( i < 10 ) printf("%d->%d\n",i,SQ[i]) ;
    }
}

void Decomp( int N )
{
    int i0,i1,i2,i3,i4 ;
    int d0,d1,d2,d3,d4 ;
    
    //  Primary
    for (i0=0;i0<MAX_MM;++i0) {
        d0 = N - SQ[i0] ;
        if ( d0 < 0 ) break ;
        if ( d0 == 0 ) {
            printf( "%8d\n",i0+1 ) ;
            return ;
        }
    }
    //  Secondary
    for (i0=0;i0<MAX_MM;++i0) {
        d0 = N - SQ[i0];
        if ( d0 < 0 ) break ;
        for ( i1=0;i1<=i0;++i1) {
            d1 = d0 - SQ[i1] ;
            if  ( d1 < 0 ) break ;
            if ( d1 == 0 ) {
                printf( "%8d,%8d\n",i0+1,i1+1 ) ;
                return ;
            }
        }
    }
    //  Tertiary
    for (i0=0;i0<MAX_MM;++i0) {
        d0 = N - SQ[i0];
        if ( d0 < 0 ) break ;
        for ( i1=0;i1<=i0;++i1) {
            d1 = d0 - SQ[i1] ;
            if  ( d1 < 0 ) break ;
            for ( i2=0;i2<=i1;++i2) {
                d2 = d1 - SQ[i2] ;
                if  ( d2 < 0 ) break ;
                if ( d2 == 0 ) {
                    printf( "%8d,%8d,%8d\n",i0+1,i1+1,i2+1 ) ;
                    return ;
                }
            }
        }
    }
    //  Quad
    for (i0=0;i0<MAX_MM;++i0) {
        d0 = N - SQ[i0];
        if ( d0 < 0 ) break ;
        for ( i1=0;i1<=i0;++i1) {
            d1 = d0 - SQ[i1] ;
            if  ( d1 < 0 ) break ;
            for ( i2=0;i2<=i1;++i2) {
                d2 = d1 - SQ[i2] ;
                if  ( d2 < 0 ) break ;
                for ( i3=0;i3<=i2;++i3) {
                    d3 = d2 - SQ[i3] ;
                    if  ( d3 < 0 ) break ;
                    if ( d3 == 0 ) {
                        printf( "%8d,%8d,%8d,%8d\n",i0+1,i1+1,i2+1,i3+1 ) ;
                        return ;
                    }
                }
            }
        }
    }
    //  Quint
    for (i0=0;i0<MAX_MM;++i0) {
        d0 = N - SQ[i0];
        if ( d0 < 0 ) break ;
        for ( i1=0;i1<=i0;++i1) {
            d1 = d0 - SQ[i1] ;
            if  ( d1 < 0 ) break ;
            for ( i2=0;i2<=i1;++i2) {
                d2 = d1 - SQ[i2] ;
                if  ( d2 < 0 ) break ;
                for ( i3=0;i3<=i2;++i3) {
                    d3 = d2 - SQ[i3] ;
                    if  ( d3 < 0 ) break ;
                    for ( i4=0;i4<=i3;++i4) {
                        d4 = d3 - SQ[i4] ;
                        if  ( d4 < 0 ) break ;
                        if ( d4 == 0 ) {
                            printf( "%8d,%8d,%8d,%8d,%8d\tQuint \n",i0+1,i1+1,i2+1,i3+1,i4+1 ) ;
                            return ;
                        }
                    }
                }
            }
        }
    }
    printf("\tOverflow!!\n");
}

int small_decomp( int N, int lim, int depth_left, int * loc )
{
    int i ;
    int d;
    //printf("\ndepth %d N %d  ",depth_left,N);
    for (i=0 ; i<= lim ; ++i ) {
        d = N - SQ[i] ;
        if (d<0) return -1 ;
        if ( depth_left == 0 ) {
            if ( d==0 ) {
                loc[0] = i+1 ;
                return 0 ;
            }
        } else {
            if ( d==0 ) return -1 ;
            loc[0] = i+1 ;
            if ( small_decomp( d, i, depth_left-1, loc+1 ) == 0 ) return 0 ;
        }
    }
    return -1 ;
}
            

int big_decomp( int N, int depth )
{
    int j ;
    int dp ;
    int components[depth] ;
    
    for ( dp = 0 ; dp < depth ; ++dp ) {
        //printf("\n Try Depth %d N=%d",dp,N);
        if ( small_decomp( N, MAX_MM-1, dp, components ) == 0 ) {
            for (j=0;j<=dp;++j) printf(",%8d",components[j]) ;
            printf("\n") ;
            return 0 ;
        }
    }
    printf("\tGreater than %d components\n",depth ) ;
    return -1 ;
}

    

int main( int argc, char ** argv )
{
    int i;
    SetupSQ() ;
    for (i=1;i<MAX_NN;++i) {
        printf("%8d",i);
 //       Decomp(i);
        big_decomp( i , 10 ) ;
    }
    return 0 ;
    
}
