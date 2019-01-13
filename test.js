var a = 10;
a++;
console_log(a);
a--;
console_log(a);

function foo(a, b) {
    var c = 100;
    console_log(a);
    console_log(b);
    console_log(c)
};

function bar() {
    var i = 1000;
    console_log(i);
    console_log(a)
};

var i = 0;
console_log(a == i);

while(i <= 10) {
    console_log(i);
    i++
};

foo(i, 200);
bar();
console_log(a);
console_log(c)