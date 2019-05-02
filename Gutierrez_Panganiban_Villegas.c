#include <stdio.h>

int TRUE = 1;
int FALSE = 0;

void printBoard(int N, int board[][N]){
	for(int i = 0 ; i < N; i++){
		for(int j = 0 ; j < N; j++){
			printf("%d ", board[i][j]);
		}
		printf("\n");
	}	
}

void printStack(int N, int stack[]){
	printf("stack:");
	for(int i = 0; i < N; i++){
		printf("%d ", stack[i]);
	}
	printf("\n");
}

void printCands(int N, int cands[][N]){
	for(int i = 0 ; i < N; i++){
		for(int j = 0 ; j < N; j++){
			printf("%d ", cands[i][j]);
		}
		printf("\n");
	}	
}

void initCands(int N, int cands[][N]){
	for(int i = 0 ; i < N; i++){
		for(int j = 0 ; j < N; j++){
			cands[i][j] = -1;
		}
	}	
}

int canPlace(int N, int board[][N], int sI, int col){
	// printf("%d , %d \n", sI, col);
	// row
	for(int i = 1; i < N-1; i++){
		if(board[sI][i] == 1){
			// printf("x\n");
			return FALSE;
		}
	}

	// col
	for(int i = 1; i < N-1; i++){	
		if(board[i][col] == 1){
			// printf("y\n");
			return FALSE;
		}
	}


	if(sI-2 > 0 && col-1 > 0 && board[sI-2][col-1] == 1){
		// printf("a\n");
		return FALSE;		
	}

	if(sI-2 > 0 && col+1 < N-1 && board[sI-2][col+1] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI+2 < N-1 && col-1 > 0 && board[sI+2][col-1] == 1){
		// printf("c\n");
		return FALSE;		
	}

	if(sI+2 < N-1 && col+1 > 0 && board[sI+2][col+1] == 1){
		// printf("d\n");
		return FALSE;		
	}

	if(sI-1 > 0 && col-2 > 0 && board[sI-1][col-2] == 1){
		// printf("e\n");
		return FALSE;		
	}

	if(sI-1 > 0 && col+2 < N-1 && board[sI-1][col+2] == 1){
		// printf("f\n");
		return FALSE;		
	}

	if(sI+1 < N-1 && col-2 > 0 && board[sI+1][col-2] == 1){
		// printf("g\n");
		return FALSE;		
	}

	if(sI+1 < N-1 && col+2 < N-1 && board[sI+1][col+2] == 1){
		// printf("h\n");
		return FALSE;		
	}

	return TRUE;
}

int isInitial(int sI, int iS, int initials[][2]){
	for(int i = 0; i < iS; i++){
		if(sI == initials[i][0]){
			return TRUE;
		}
	}
	return FALSE;
}

int searchInitial(int sI, int iS, int initials[][2]){
	for(int i = 0; i < iS; i++){
		if(sI == initials[i][0]){
			return initials[i][1];
		}
	}
}

int isInitialBoardValid(int N, int board[][N], int iS, int initials[][2]){
	
	// for(int i = 0; i < iS; i++){
	// 	printf("%d %d\n", initials[iS]);
	// }
	for(int i = 0 ; i < iS; i++){
		int row = initials[i][0];
		int col = initials[i][1];
		if(canPlace(N, board, row, col) == TRUE){
			board[row][col] = 1;
		}
		else{
			return FALSE;
		}
	}
	return TRUE;
}

void nchancellors(int N, int board[][N+2], int stack[], int cands[][N+2], int iS, int initials[][2]){

	int solution = 0;
	int sI, start;
	sI = start = 0;

	stack[start] = 1; 

	while(stack[start] > 0){
		// if(sI > 10){
		// 	printf("stop\n");
		// 	return;
		// }
		if(sI == N+1){ // soln found
			solution++;
			printf("-------------------------------:\n");
			printf("solution %d\n", solution);

			for(int i = 1; i < N+1; i++){
				printf("%d, %d \n", i , cands[i][stack[i]]);
			}

			printf("-------------------------------:\n");
		}

		if(stack[sI] > 0){ // get next row
			if(sI != 0){
				board[sI][cands[sI][stack[sI]]] = 1;
			}

			sI++;
			if(isInitial(sI, iS, initials) == FALSE){
				stack[sI] = 0; 

				for(int col = N; col >= 1; col--){  // find cands
					if(canPlace(N+2, board, sI, col) == TRUE){
						stack[sI]++;
						cands[sI][stack[sI]] = col;					
					}
				}
				// printf("cands have been put in the arr\n");	
			}
			else{
				stack[sI] = 1;
				// printf("cands col: %d\n", sI);
				// printf("initials\n");

				int col = searchInitial(sI, iS, initials);
				cands[sI][stack[sI]] = col;
				// printf("col: %d\n", cands[sI][stack[sI]]);
				// printf("isInitial %d\n", sI);
			}
		}	
		else{ // pop
			// printf("time to pop\n");
			sI--;
			if(isInitial(sI, iS, initials) == TRUE){
				sI--;
				board[sI][cands[sI][stack[sI]]] = 0;
				stack[sI]--;
				continue;
			}
			board[sI][cands[sI][stack[sI]]] = 0;
			stack[sI]--;
		}
		// printf("sI: %d\n", sI); 
		// printBoard(N+2, board);
		// printStack(N+2, stack);
		// printCands(N+2, cands);

	}

	if(stack[start] == 0 && solution == 0){
		printf("No solutions");
	}

}

void initBoard(int N, int board[][N]){
	for(int i = 0 ; i < N; i++){  // init
		for(int j = 0 ; j < N; j++){
			if(i == 0 || j == 0 || i == N-1 || j == N-1){
				board[i][j] = 9;
			}
			else{
				board[i][j] = 0;
			}
		}
	}
}

void initStack(int N, int stack[]){
	for(int i = 0; i < N+2; i++){ // init stack
		stack[i] = 0; 
	}
}
int main(int argc, char const *argv[]){

	char filename[10] = "input.in";
	FILE *fp;
	fp = fopen(filename, "r");

	int N;
	int puzzlenum;

	// scan for number of puzzles to read
	fscanf(fp, "%d\n", &puzzlenum);

	// loop through each puzzle config
	for (int p = 0; p < puzzlenum; p++){

		// get the size of the board
		fscanf(fp, "%d\n", &N);

		// init the board and stack with size N+2
		int board[N+2][N+2];
		int stack[N+2];
		int cands[N+2][N+2];

		initBoard(N+2, board);
		initStack(N, stack);
		initCands(N+2, cands);

		int maxInitials = N*N;
		int initials[maxInitials][2];
		int iS = 0;
		int val = 0;

		// get the inital points
		for(int i = 0; i < N; i++){
			for (int j = 0; j < N; j++){
				fscanf(fp, "%d ", &val); 
				if(val == 1){
					initials[iS][0] = i+1;   // row of initial
					initials[iS][1] = j+1;   // col
					iS++;
				}
			}
		} 

		if(isInitialBoardValid(N+2, board, iS, initials) == FALSE){
			printf("Puzzle %d\n", p+1);  
			printf("No solutions\n");
			continue;
		}
		printf("Puzzle %d\n", p+1);  
		nchancellors(N, board, stack, cands, iS, initials);
	}
}

