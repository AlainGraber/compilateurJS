function f(x) {
  return x + 0.1;
}

var i = 0;

while (i < 10) {
  console_log(i);
  console_log(f(i));
  i++;
}