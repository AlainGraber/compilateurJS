function foo() {
    a = 1; // Like ES5 in unstrict mode, this variable will become global since the var keyword is not used
    var b = 2; // This variable will only be accessible in the local (function) scope since it was declared with the var keyword
}

foo();
console_log(a); // Variable a is accessible even if it was declared in the function -> did not use var keyword
// The statement below will throw an error
console_log(b); // Variable b doesn't exist in this scope, it was declared with the var keyword in the function scope
