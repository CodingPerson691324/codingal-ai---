#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"=== Number Guessing Game ===");
        NSLog(@"I'm thinking of a number between 1 and 100.");
        
        int secretNumber = arc4random_uniform(100) + 1;
        int guess = 0;
        int attempts = 0;
        
        while (guess != secretNumber) {
            NSLog(@"Enter your guess:");
            scanf("%d", &guess);
            attempts++;
            
            if (guess < secretNumber) {
                NSLog(@"Too low! Try again.");
            } else if (guess > secretNumber) {
                NSLog(@"Too high! Try again.");
            } else {
                NSLog(@"Correct! You got it in %d attempts!", attempts);
            }
        }
    }
    return 0;
}