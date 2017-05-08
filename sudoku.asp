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

%inbox(1, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y < 4.
%inbox(2, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y < 7, Y > 3.
%inbox(3, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X < 4, Y > 6.

%inbox(4, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y < 4.
%inbox(5, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y < 7, Y > 3.
%inbox(6, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 3, X < 7, Y > 6.

%inbox(7, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y < 4.
%inbox(8, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y < 7, Y > 3.
%inbox(9, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), X > 6, Y > 6.

%inbox(W, Z) :- num(Z), grid(X, Y, Z), row(X), col(Y), W = ((((((X - 1) / 3) * 9) + ((Y - 1) / 3) + 1)) \ 9) + 1.


%:- row(X), col(Y), num(Z), num(ZZ), grid(X,Y,Z), grid(X,Y,ZZ), Z != ZZ.

%1 { grid(X, Y, Z) : row(X) } 1 :- col(Y), num(Z).
%1 { grid(X, Y, Z) : col(Y) } 1 :- row(X), num(Z).
%1 { inbox(W, Z) : box(W) } 1 :- num(Z).
%1 { inbox(W, Z) : num(Z) } 1 :- box(W).

%#show grid/3.
%#show blank/2.
#show inbox/2.