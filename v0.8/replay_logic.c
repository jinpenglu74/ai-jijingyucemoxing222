#include "replay_logic.h"

static int is_digit_r(u16 c){return c>='0'&&c<='9';}
static int valid_time_r(const u16* s){
    if(!s)return 0;
    return is_digit_r(s[0])&&is_digit_r(s[1])&&is_digit_r(s[2])&&is_digit_r(s[3])&&
           s[4]=='-'&&is_digit_r(s[5])&&is_digit_r(s[6])&&s[7]=='-'&&
           is_digit_r(s[8])&&is_digit_r(s[9]);
}
int replay_time_text_leq(const u16* a,const u16* b){
    int i=0;
    if(!valid_time_r(a)||!valid_time_r(b))return 0;
    while(a[i]&&b[i]&&a[i]==b[i])i++;
    if(!a[i])return 1;
    if(!b[i])return 0;
    return a[i]<b[i];
}
int replay_date_available(int available_yyyymmdd,int replay_yyyymmdd){
    if(available_yyyymmdd<=0||replay_yyyymmdd<=0)return 0;
    return available_yyyymmdd<=replay_yyyymmdd;
}
