// Example which shows the local (function) scope and shadowing of global variables
var a = 1;

function foo() {
    var a = 2; // Declaration : shadows the global variable in the function scope
    console_log(a);
}

function bar() {
    a = 3; // Assignation : changes the value of the global variable
    console_log(a);
}

console_log(a); // Should output 1
foo(); // Should output 2
console_log(a); // Should output 1, foo() did not change the value of a

console_log(a); // Should output 1
bar(); // Should output 3
console_log(a); // Should output 3, bar() did change the value of a