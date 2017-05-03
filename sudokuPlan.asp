%Wolf, Goat, Cabbage problem

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Solution (for checking): %
%	1. Bring goat      %
%	2. Go back alone   %
%	3. Bring cabbage   %
%	4. Bring back goat %
%	5. Bring wolf      %
%	6. Go back alone   %
%	7. Bring goat      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%% A: Define Time
time(1..43).
ptime(1..42).
row(1..9).
col(1..9).
box(1..9).
num(1..9).


%%%% B: Define Fluents
fluent(grid(X, Y, Z)) :- row(X), col(Y), num(Z).
fluent(inrow(X, Z)) :- row(X), num(Z).
fluent(incol(Y, Z)) :- col(Y), num(Z).
fluent(inbox(W, Z)) :- box(Y), num(Z).
fluent(blank(X, Y)) :- row(X), col(Y).


%%%% C: Define Actions
action(fill(X, Y, Z)) :- row(X), col(Y), num(Z).


%%%% D: Define What is initially true and map it to time 0 or time 1
%Row 1
initially(grid(1, 1, 8)).
initially(grid(1, 2, 1)).
initially(grid(1, 3, 3)).
initially(grid(1, 6, 9)).
initially(grid(1, 7, 5)).
initially(grid(1, 9, 4)).
%Row 2
initially(grid(2, 6, 3)).
initially(grid(2, 7, 7)).
initially(grid(2, 9, 8)).
%Row 3
initially(grid(3, 1, 9)).
initially(grid(3, 3, 4)).
initially(grid(3, 5, 2)).
initially(grid(3, 7, 1)).
%Row 4
initially(grid(4, 1, 6)).
initially(grid(4, 2, 5)).
initially(grid(4, 3, 7)).
initially(grid(4, 4, 9)).
initially(grid(4, 5, 4)).
%Row 5
initially(grid(5, 4, 3)).
initially(grid(5, 5, 7)).
initially(grid(5, 6, 2)).
%Row 6
initially(grid(6, 5, 5)).
initially(grid(6, 6, 6)).
initially(grid(6, 7, 9)).
initially(grid(6, 8, 7)).
initially(grid(6, 9, 1)).
%Row 7
initially(grid(7, 3, 8)).
initially(grid(7, 5, 3)).
initially(grid(7, 7, 2)).
initially(grid(7, 9, 9)).
%Row 8
initially(grid(8, 1, 7)).
initially(grid(8, 3, 6)).
initially(grid(8, 4, 1)).
%Row 9
initially(grid(9, 1, 3)).
initially(grid(9, 3, 1)).
initially(grid(9, 4, 2)).
initially(grid(9, 7, 6)).
initially(grid(9, 8, 4)).
initially(grid(9, 9, 7)).

filled(X, Y) :- row(X), col(Y), num(Z), grid(X, Y, Z).
initially(blank(X, Y)) :- row(X), col(Y), not filled(X, Y).

h(F,1) :- initially(F), fluent(F).
h(n(F),1) :- fluent(F), not initially(F).


%%%% E: Express the effect of actions
%fill(X, Y, Z) causes grid(X, Y, Z)
h(grid(X, Y, Z), T + 1) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).
ab(n(grid(X, Y, Z)), T) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).

%fill(X, Y, Z) causes ~blank(X, Y).
h(n(blank(X, Y)), T + 1) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y).
ab(blank(X, Y), T) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y).

%fill(X, Y, Z) causes inrow(X, Z).
h(inrow(X, Z), T + 1) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).
ab(n(inrow(X, Z)), T) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).

%fill(X, Y, Z) causes incol(Y, Z).
h(incol(Y, Z), T + 1) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).
ab(n(incol(Y, Z)), T) :- o(fill(X, Y, Z), T), time(T), row(X), col(Y), num(Z).


%%%% F: For reasoning about action occurrences; list the action occurrences
%%%% 	For planning, skip this part


%%%% G: Intertia Actions
h(F,T+1) :- h(F,T), not ab(F,T), fluent(F), time(T).
h(n(F),T+1) :- h(n(F),T), not ab(n(F),T), fluent(F), time(T).

%% To do planning remove the action occurrences above
%% and uncomment the following three rules in H, I, and J.

%%%% H: Define the Goal
%goal(T) :- h(n(blank(X, Y)), T) time(T), row(X), col(Y), num(Z).


%%%% I: Write the constraint to enforce that your goal is satisfied at your desired time
:- not goal(43).


%%%% J: Enumerate action occurrence
1 {o(A,T): action(A)} 1 :- ptime(T).


%%%% K: Express the executability conditions
%executable fill(X, Y, Z) if blank(X, Y), .



%executable lonestart(X) if ~startside(X).
exec(lonestart(X), T) :- time(T), passenger(X), h(n(startside(X)), T),  X = sailor.

%executable lonegoal(X) if startside(X).
exec(lonegoal(X), T) :- time(T), passenger(X), h(startside(X), T),  X = sailor.

%executable gostart(X, Y) if ~startside(X), ~startside(Y).
exec(gostart(X, Y), T) :- time(T), passenger(X), passenger(Y), h(n(startside(X)), T), h(n(startside(Y)), T),  X = sailor.

%executable gogoal(X, Y) if startside(X), startside(Y).
exec(gogoal(X, Y), T) :- time(T), passenger(X), passenger(Y), h(startside(X), T), h(startside(Y), T),  X = sailor.


%%%% L: Write the constraint that says only actions that are executable can occur
:- action(A), time(T), not exec(A,T), o(A,T).

#show o/2.
%#show h/2.