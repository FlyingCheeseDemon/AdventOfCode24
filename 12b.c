#include <stdio.h>
#include <stdbool.h>

int GRID_DIM = 140;

void floodfill_step(int start_position[],char grid[GRID_DIM][GRID_DIM],int grid_dim);

void print_grid(char grid[GRID_DIM][GRID_DIM],int dim_grid);

int evaluate_area(char grid[GRID_DIM][GRID_DIM],int grid_dim);

int main() {
    FILE *fptr;
    fptr = fopen("12-input.txt", "rt"); 
    // not sure how to get this programmatically yet
    int dim_grid = GRID_DIM;

    char field[dim_grid*dim_grid];
    int index = 0;

    char currentChar;
    // read file to grid:
    while((currentChar = fgetc(fptr)) != EOF) {
        if(currentChar >= 65){
            field[index] = currentChar;
            index++;
        }
    }
    char grid[dim_grid][dim_grid];
    for(int i = 0;i<dim_grid;i++){
        for(int j = 0;j<dim_grid;j++){
            index = dim_grid*i+j;
            grid[i][j] = field[index];
            // printf("%c",grid[i][j]);
        }
        // printf("\n");
    }

    // iterate through the grid and for every cell try to floodfill the area to detect connected fields
    // during floodfill mark all letters in the same area by making them lowercase
    // a = 0110 0001
    // A = 0100 0001
    // then go though the lowercase letters to determine area and perimeter
    // then make all the lowercase characters something else to discard them
    // Make them 1000 0000 (128)
    int fence = 0;
    for(int i = 0;i<dim_grid;i++){
        for(int j = 0;j<dim_grid;j++){
            char letter = grid[i][j];
            int invalid = letter == 0b01000000;
            if(invalid){ // check if 128
                continue;
            }
            int lowercase = letter & 0b000100000;
            if(!lowercase){
                int position[2] = {i,j};
                floodfill_step(position,grid,dim_grid);
                print_grid(grid,dim_grid);
                int value = evaluate_area(grid,dim_grid);
                fence += value;
            }
        }
    }
    printf("\nSolution:%d\n\n", fence); //865708 too low
    return 0;
}

void floodfill_step(int position[],char grid[GRID_DIM][GRID_DIM],int grid_dim){

    char letter = grid[position[0]][position[1]];
    grid[position[0]][position[1]] = letter | 0b00100000; // to lowercase

    int directions[4][2] = {{-1,0},{0,-1},{0,1},{1,0}};
    for(int d = 0;d<4;d++){
        int next_position[] = {position[0]+directions[d][0],position[1]+directions[d][1]};
        char next_char = grid[next_position[0]][next_position[1]];
        if(next_char == letter && next_position[0] >= 0 && next_position[1] >= 0 && next_position[0] < grid_dim && next_position[1] < grid_dim){
            floodfill_step(next_position, grid, grid_dim);
        }
    }

}

int evaluate_area(char grid[GRID_DIM][GRID_DIM],int grid_dim){
    int area = 0;
    int perimeter = 0;

    for(int i = 0;i<grid_dim;i++){
        for(int j = 0;j<grid_dim;j++){
            char letter = grid[i][j];
            int test = letter & 0b00100000;
            if(test == 32 ){ //lowercalse
                area++;
            }
        }
    }

    // we go through all adjacent column pairs first.
    // treating out of bounds as 0
    bool letter_1;
    bool letter_2;
    int cntr = 0;
    
    // rows
    for(int i = -1;i<grid_dim;i++){
        bool status_previous_wall = false;
        bool previous_wall_left = false; // means letter 1 was true
        for(int j = 0;j<grid_dim;j++){ // line
            if (i == -1){
                letter_1 = false;
            } else {
                letter_1 = grid[i][j] & 0b00100000; // lowercase yes
            }
            if (i == grid_dim-1){
                letter_2 = false;
            } else {
                letter_2 = grid[i+1][j] & 0b00100000;
            }
            bool status_this_wall = (letter_1 ^ letter_2); // exactly one of the two is true
            if (status_this_wall){
                if (!status_previous_wall){
                    cntr += 1;
                }else{
                    if(letter_1 ^ previous_wall_left){ // swapping orientation
                        cntr += 1;
                    }
                }
            }
            status_previous_wall = status_this_wall;
            previous_wall_left = letter_1;
        }
    }
    printf("%d, ",cntr);
    // columns
    for(int i = -1;i<grid_dim;i++){
        bool status_previous_wall = false;
        bool previous_wall_left = false; // means letter 1 was true
        for(int j = 0;j<grid_dim;j++){ // line
            if (i == -1){
                letter_1 = false;
            } else {
                letter_1 = grid[j][i] & 0b00100000; // lowercase yes
            }
            if (i == grid_dim-1){
                letter_2 = false;
            } else {
                char test = grid[j][i+1];
                int test2 = grid[j][i+1] & 0b00100000;
                letter_2 = test2;
            }
            bool status_this_wall = (letter_1 ^ letter_2); // exactly one of the two is true
            if (status_this_wall){
                if (!status_previous_wall){
                    cntr += 1;
                }else{
                    if(letter_1 ^ previous_wall_left){ // swapping orientation
                        cntr += 1;
                    }
                }
            }
            status_previous_wall = status_this_wall;
            previous_wall_left = letter_1;
        }

    }
    int test;
    for(int i = 0;i<grid_dim;i++){
        for(int j = 0;j<grid_dim;j++){
            char letter = grid[i][j];
            test = letter & 0b00100000;
            if(test == 32){ //lowercalse
                grid[i][j] = 0b01000000; 
            }
        }
    }
    printf("%d\n",cntr);
    printf("area: %d\n",area);
    return area*cntr;

}

void print_grid(char grid[GRID_DIM][GRID_DIM],int dim_grid){
    for(int i = 0;i<dim_grid;i++){
        for(int j = 0;j<dim_grid;j++){
            printf("%c",grid[i][j]);
        }
        printf("\n");
    }
    // printf("\n");
}