#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
const ll p= 998244353;

struct poly
{
    ll a[510];
    int n;
    poly()
    {
        memset(a,0,sizeof a);
        n=0;
    }
    ll &operator [](int x)
    {
        return a[x];
    }
};
int n, Q;
ll a[510][510];
void add(poly &a,poly &b,pll c)
{
    a.n=max(a.n,b.n+bool(c.first));
    int i;
    for(i=0;i<=a.n;i++)
    {
        a[i]=(a[i]+b[i]*c.second)%p;
        if(i)
            a[i]=(a[i]+b[i-1]*c.first)%p;
    }
}
ll fp(ll a,ll b)
{
    ll s=1;
    for(;b;b>>=1,a=a*a%p)
        if(b&1)
            s=s*a%p;
    return s;
}
void gao1()
{
    int i,j,k;
    for(i=1;i<=n;i++)
    {
        for(j=i+1;j<=n;j++)
            if(a[i][j])
                break;
        if(j>n)
            continue;
        if(j!=i+1)
        {
            for(k=i;k<=n;k++)
                swap(a[i+1][k],a[j][k]);
            for(k=1;k<=n;k++)
                swap(a[k][i+1],a[k][j]);
        }
        ll e=fp(a[i+1][i],p-2);
        for(j=i+2;j<=n;j++)
            if(a[j][i])
            {
                ll v=e*a[j][i]%p;
                for(k=i;k<=n;k++)
                    a[j][k]=(a[j][k]-a[i+1][k]*v)%p;
                for(k=1;k<=n;k++)
                    a[k][i+1]=(a[k][i+1]+a[k][j]*v)%p;
            }
    }
}
pll c[510][510];
poly f[510];
pll operator *(pll a,pll b)
{
    return pll((a.first*b.second+a.second*b.first)%p,a.second*b.second%p);
}
pll operator *(pll a,ll b)
{
    return pll(a.first*b%p,a.second*b%p);
}
void gao2()
{
    f[n+1][0]=1;
    int i,j;
    for(i=n;i>=1;i--)
    {
        pll v(0,1);
        for(j=i+1;j<=n+1;j++)
        {
            add(f[i],f[j],v*c[i][j-1]*((j-i)&1?1:-1));
            v=v*c[j][j-1];
        }
    }
}

ll charp[510], qry;

ll calc(ll q){ //calculate n
    ll ans = charp[n];
    for(int i = n - 1; i >= 0; i--){
        ans = (ans*q + charp[i])%p;
    }
    return ans;
}

int main()
{
    // ios_base::sync_with_stdio(false);
    // cin.tie(NULL);
    n = 400;
    Q = 0;
    cin >> n;
    int i,j;
    for(i=1;i<=n;i++)
        for(j=1;j<=n;j++)
            cin >> a[i][j];
    // for(int i = 0; i < n; i++){
    //     for(int j = 0; j < n; j++){
    //         a[i][j] = rand()%10;
    //     }
    // }
    gao1();
    for(i=1;i<=n;i++)
        for(j=1;j<=n;j++)
        {
            c[i][j].second=-a[i][j];
            if(i==j)
                c[i][j].first=1;
        }
    gao2();
    for(int i = 0; i < n + 1; i++){
        charp[i] = (f[1][i]+p)%p;
        charp[i] = n%2 ? -charp[i] + p : charp[i];
    }
    // cout << "done\n";
    for(int i = 0; i < n +1; i++) cout << charp[i] << "!" << charp[i] - p << '\n';
    while(Q--){
        cin >> qry;
        cout << calc(qry) << ' ';
    }
    cout.flush();
    
}