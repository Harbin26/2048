# 2048


@)48 implmentation using BFS.


We are at the middle of 2048 game and 8 places (on the 4x4 board) are filled with random numbers (valid for 2048 game).

Use BFS to look for the best first three moves that maximizes the expected score. Note that there are 4 actions that you can take: Move Up, Move Down, Move Right, and Move Left. This first move results in some score (let's call it S1). After this move, the game add a 2 or a 4 at a randomly selected empty location. To keep this milestone as simple as possible, let's assume that a "2" is added to the first empty location that is found in vertical scan from top to bottom of the board. Then we take another action, which results in some other score (let's call is S2). After this move, the game add a 2  to the first empty location that is found in vertical scan from top to bottom of the board. After that, we take our third action, which results in some other score (let's call is S3). We want to select the actions that maximizes S1+S2+S3.

 

Example
We have the following initial arrangement:

2	4	4	
16			
4	8		
2	8		
If we move left, we have:

2	8		
16			
4	8		
2	8		
And S1 is 8.

Then, a 2 is added in the fits empty place that is found in a vertical scan from top left to the bottom right:

2	8	2	
16			
4	8		
2	8		
If we move down, we have:

2			
16			
4	8		
2	16	2	
And S2 is 16.

Then, a 2 is added in the fits empty place that is found in a vertical scan from top left to the bottom right:

2	2		
16			
4	8		
2	16	2	
And if we move up, we have:

2	2	2	
16	8		
4	16		
2			
And S3 is zero.

 

Programming language
Any language is OK.

 

Input
Read the initial arrangements from a file called "2048_in.txt". The file starts with N, number of test cases. Then there are 4N lines, 4 lines for each test case. On each line we have four numbers separated by comma. For empty places put a zero.

 

Output
Print the output in a file called "2048_out.txt". For each test case, print the maximum score and then three moves (use L for left, R for right, U for up, and D for down). Separate each value (score and the moves) with a comma.

 

Example input file:
1

2,4,4,0

16,0,0,0

4,8,0,0

2,8,0,0

 

Example output file:
24,L,D,U
