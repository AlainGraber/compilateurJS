// This example shows the return statement in a function
function foo(x, y) {
    return x + y;

    // Code below is unreachable
    console_log(x);
    console_log(y);
}

var a = 1;
var b = 2;
var c = foo(a, b);

console_log(c);