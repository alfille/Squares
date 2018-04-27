#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>


// Program to find best sum of squares for all integers

#define MAX_N 100 // max integer (squared)
#define MAX_M MAX_N // max covering square

#define MAX_DEPTH 10

struct global {
    long long int * SQ ;
    int n ;
    int m ;
    long long int nn ;
    long long int mm ;
    int depth ;
    int count ;
    int power ;
} Global = { NULL, MAX_N, MAX_M, 0, 0, MAX_DEPTH, 0, 2 } ;
    

long long int power( int value )
{
    int p ;
    long long int result = value ;
    for ( p=Global.power; p>1 ; --p ) {
        result *= value ;
    }
    return result ;
}

void SetupSQ( void )
{
    int i;
    Global.mm = power(Global.m);
    Global.nn = power(Global.n);
    Global.SQ = calloc( Global.mm, sizeof(Global.SQ[0]) ) ;
    if (Global.SQ==NULL) exit(1) ;
    for ( i=0 ; i<Global.mm ; ++i ) {
        Global.SQ[i] = power(i+1);
        if ( i < 10 ) printf("%d->%lld\n",i,Global.SQ[i]) ;
    }
}

int small_decomp( long long int N, int lim, int depth_left, long long int * loc )
{
    int i ;
    long long int d;
    //printf("\ndepth %d N %d  ",depth_left,N);
    for (i=0 ; i<= lim ; ++i ) {
        d = N - Global.SQ[i] ;
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
            

int big_decomp( long long int N )
{
    int dp ;
    long long int components[Global.depth] ;
    
    for ( dp = 0 ; dp < Global.depth ; ++dp ) {
        //printf("\n Try Depth %d N=%d",dp,N);
        if ( small_decomp( N, Global.mm-1, dp, components ) == 0 ) {
            if ( Global.count == 0 ) {
                int j ;
                for (j=0;j<=dp;++j) printf(",%8lld",components[j]) ;
                printf("\n") ;
            } else {
                printf( ",%8d\n",dp+1);
            }
            return 0 ;
        }
    }
    if ( Global.count == 0 ) {
        printf("\tGreater than %d components\n",Global.depth ) ;
    } else {
        printf( ", >%7d\n",Global.depth) ;
    }
    return -1 ;
}

void usage( char * prog )
{
    printf( "Sum-of-squares decomposition: Find the minimum number of integer squares thqt sum to a given number\n");
    printf( "\t{c} 2018 Paul H Alfille see github.com\n" );
    printf( "Usage %s number\n",prog);
    printf( "\tlook for sums up to <number> squared (default 100)\n");
    printf( "\t-m --max max_number used for squares\n");
    printf( "\t-d --depth max number of squares summed (default 10)\n");
    printf( "\t-3 --cube look for cubed number sums\n" );
    printf( "\t-4 --fourth power sums\n");
    printf( "\t-5 --fifth power sums\n");
    printf( "\t-6 --sixth power sums\n");
    printf( "\t-p --power up to 10th\n");
    printf( "\t-c --count number of terms rather than list them\n");
    printf( "\t-h --help this summary\n") ;
    exit(0) ;
}


void commandline( int argc, char * argv[] )
{
    // options

    int opt ;
    int long_index = 0 ; // dummy
    static struct option long_opts[] = {
        { "max", required_argument, 0, 'm' },
        { "depth", required_argument, 0, 'd' } ,
        { "cube", no_argument, 0, '3' } ,
        { "fourth", no_argument, 0, '4' } ,
        { "fifth", no_argument, 0, '5' } ,
        { "sixth", no_argument, 0, '6' } ,
        { "count", no_argument, 0, 'c' } ,
        { "power", required_argument, 0, 'p' } ,
        { "help", no_argument, 0, 'h' } ,
        { 0, 0, 0, 0, },
    } ;
    while ( (opt=getopt_long(argc, argv, "m:d:p:3456ch", long_opts, &long_index)) != -1){
        switch (opt) {
            case 'm':
				if ( optarg != NULL ) {
					 Global.m = atoi(optarg) ;
				} else {
					fprintf(stderr,"Option %c needs a following value -- ignoring\n",opt);
				}
                break ;
            case 'd':
				if ( optarg != NULL ) {
					 Global.depth = atoi(optarg) ;
				} else {
					fprintf(stderr,"Option %c needs a following value -- ignoring\n",opt);
				}
                break ;
            case 'p':
				if ( optarg != NULL ) {
                    Global.power = atoi(optarg) ;
                    if (Global.power > 10) {
                        fprintf(stderr,"Power too large %d > 10\n",Global.power) ;
                        exit(1) ;
                    } else if ( Global.power < 1 ) {
                        fprintf(stderr,"Power too small %d < 1\n",Global.power) ;
                        exit(1) ;
                    }
				} else {
					fprintf(stderr,"Option %c needs a following value -- ignoring\n",opt);
				}
                break ;
            case '3':
                Global.power = 3 ;
                break ;
            case '4':
                Global.power = 4 ;
                break ;
            case '5':
                Global.power = 4 ;
                break ;
            case '6':
                Global.power = 4 ;
                break ;
            case '?':
            case 'h':
                usage(argv[0]);
                exit(0);
            case 'c':
                Global.count = 1 ;
                break ;
            default:
                usage(argv[0]) ;
                exit(1);
        }
    }
    
    if ( optind < argc ) {
		Global.n = atoi( argv[optind] ) ;
	}

}
    

int main( int argc, char * argv[] )
{
    int i;

    commandline( argc, argv ) ;
    SetupSQ() ;
    for (i=1;i<Global.nn;++i) {
        printf("%8d",i);
        big_decomp( i ) ;
    }
    return 0 ;
    
}
