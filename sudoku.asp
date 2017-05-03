row(1..9).
col(1..9).
box(1..9).
num(1..9).

%initially(X, Y, Z) = Initially, there is a Z in row X, column Y
%Row 1
initially(1, 1, 8).
initially(1, 2, 1).
initially(1, 3, 3).
initially(1, 6, 9).
initially(1, 7, 5).
initially(1, 9, 4).
%Row 2
initially(2, 6, 3).
initially(2, 7, 7).
initially(2, 9, 8).
%Row 3
initially(3, 1, 9).
initially(3, 3, 4).
initially(3, 5, 2).
initially(3, 7, 1).
%Row 4
initially(4, 1, 6).
initially(4, 2, 5).
initially(4, 3, 7).
initially(4, 4, 9).
initially(4, 5, 4).
%Row 5
initially(5, 4, 3).
initially(5, 5, 7).
initially(5, 6, 2).
%Row 6
initially(6, 5, 5).
initially(6, 6, 6).
initially(6, 7, 9).
initially(6, 8, 7).
initially(6, 9, 1).
%Row 7
initially(7, 3, 8).
initially(7, 5, 3).
initially(7, 7, 2).
initially(7, 9, 9).
%Row 8
initially(8, 1, 7).
initially(8, 3, 6).
initially(8, 4, 1).
%Row 9
initially(9, 1, 3).
initially(9, 3, 1).
initially(9, 4, 2).
initially(9, 7, 6).
initially(9, 8, 4).
initially(9, 9, 7).


grid(X, Y, Z) :- row(X), col(Y), num(Z), initially(X, Y, Z).
filled(X, Y) :- row(X), col(Y), num(Z), grid(X, Y, Z).

blank(X, Y) :- row(X), col(Y), not filled(X, Y).

box(1, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y < 4.
box(2, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y < 7, Y > 3.
box(3, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y > 6.

box(4, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y < 4.
box(5, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y < 7, Y > 3.
box(6, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y > 6.

box(7, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y < 4.
box(8, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y < 7, Y > 3.
box(9, Z) :- filled(X, Y), num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y > 6.


%:- row(X), col(Y), num(Z), num(ZZ), grid(X,Y,Z), grid(X,Y,ZZ), Z != ZZ.

%1 { grid(X, Y, Z) : row(X)} 1 :- col(Y), num(Z).

%#show grid/3.
%#show blank/2.
#show box/2.