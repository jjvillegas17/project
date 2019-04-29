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

int check(){

}


int pop(){

}

void push(){

}

int canPlace(int N, int board[][N], int sI, int col){
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
		// printf("b\n");
		return FALSE;		
	}

	if(sI-2 > 0 && col+1 < N-1 && board[sI-2][col+1] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI+2 < N-1 && col-1 > 0 && board[sI+2][col-1] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI+2 < N-1 && col+1 > 0 && board[sI+2][col+1] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI-1 > 0 && col-2 > 0 && board[sI-1][col-2] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI-1 > 0 && col+2 < N-1 && board[sI-1][col+2] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI+1 < N-1 && col-2 > 0 && board[sI+1][col-2] == 1){
		// printf("b\n");
		return FALSE;		
	}

	if(sI+1 < N-1 && col+2 < N-1 && board[sI+1][col+2] == 1){
		// printf("b\n");
		return FALSE;		
	}

	// 
	// if(sI-2 > 0 && col+1 < N-1 && board[sI-2][col+1] == 1){
	// 	// printf("b\n");
	// 	return FALSE;		
	// }

	// if(sI-1 > 0 && col-2 > 0 && board[sI-1][col-2] == 1){
	// 	// printf("c\n");
	// 	return FALSE;
	// }

	// if(sI-1 > 0 && col+2 < N-1 && board[sI-1][col+2] == 1){
	// 	// printf("b\n");
	// 	return FALSE;		
	// }

	// if(sI+2 < N-1 && col-1 > 0 && board[sI+2][col-1] == 1){  // pahigang L
	// 	// printf("d\n");
	// 	return FALSE;
	// }

	// if(sI+2 < N-1 && col+1 < N-1 && board[sI+2][col+1] == 1){  
	// 	// printf("d\n");
	// 	return FALSE;
	// }

	// if(sI-1 > 0 && col-2 > 0 && board[sI-1][col-2] == 1){
	// 	// printf("e\n");
	// 	return FALSE;
	// }

	// if(sI-1 > 0 && col+2 < N-1 && board[sI-1][col+2] == 1){
	// 	// printf("e\n");
	// 	return FALSE;
	// }

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
				printf("cands have been put in the arr\n");	
			}
			else{
				// place the initial config of the current sI
				stack[sI] = 1;
				printf("cands col: %d\n", sI);
				printf("initials\n");
				for(int i = 0; i < iS; i++){
					for(int j = 0; j < 2; j++){
						printf("%d ", initials[i][j]); 
					}
					printf("\n");
				}
				int col = searchInitial(sI, iS, initials);
				cands[sI][stack[sI]] = col;
				printf("col: %d\n", cands[sI][stack[sI]]);
				printf("isInitial %d\n", sI);
			}
		}	
		else{ // pop
			printf("time to pop\n");
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
		printf("sI: %d\n", sI); 
		printBoard(N+2, board);
		printStack(N+2, stack);
		printCands(N+2, cands);

		if(stack[start] == 0 && solution == 0){
			printf("No solutions");
		}
	}

}

int main(int argc, char const *argv[]){
	int N;
	printf("Enter size of board: \n");
	scanf("%d", &N);

	int board[N+2][N+2];

	for(int i = 0 ; i < N+2; i++){  // init
		for(int j = 0 ; j < N+2; j++){
			if(i == 0 || j == 0 || i == N+1 || j == N+1){
				board[i][j] = 9;
			}
			else{
				board[i][j] = 0;	
			}
		}
	}

	int stack[N+2];

	for(int i = 0; i < N+2; i++){ // init stack
		stack[i] = 0; 
	}

	int cands[N+2][N+2];
	initCands(N+2, cands);

	// if has initial chancy placed
	// 4x4
	// board[1][1] = 1;
	// cands[1][1] = 1;
	// stack[1] = 1;

	// board[2][4] = 1;
	// cands[2][1] = 4;
	// stack[2]= 1;

	// 4x4
	// board[1][4] = 1;
	// cands[1][1] = 4;
	// stack[1] = 1;

	// board[3][2] = 1;
	// cands[3][1] = 2;
	// stack[3]= 1;

	//8x8
	// board[2][7] = 1;
	// cands[2][1] = 7;
	// stack[2] = 1;

	// board[4][5] = 1;
	// cands[4][1] = 5;
	// stack[4]= 1;

	// board[5][2] = 1;
	// cands[5][1] = 2;
	// stack[5] = 1;

	// board[7][4] = 1;
	// cands[7][1] = 4;
	// stack[7]= 1;

	//8x8
	board[2][3] = 1;
	// cands[2][1] = 3;
	// stack[2] = 1;

	board[4][1] = 1;
	// cands[4][1] = 1;
	// stack[4]= 1;

	// 5x5
	// board[2][1] = 1;
	// cands[2][1] = 1;
	// stack[2] = 1;

	// board[3][2] = 1;
	// cands[3][1] = 2;
	// stack[3] = 1;

	int iS = 2;
	int initials[2][2] = { {2,3}, {4,1} };

	// printBoard(size, board);
	nchancellors(N, board, stack, cands, iS, initials);

}