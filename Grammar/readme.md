# Grammar:
In the file **grammar.ne** you find the grammar that we developed.

In the files **acceptedExample1-4.txt** you find some examples of trees that the narley parser should accept.

## How to use nearley:
1. Install nearley using: 
    ```
    $ npm install -g nearley
    ```
2. Compile the grammar that you find in the file **grammar.ne** using:
    ```
    $ nearleyc grammar.ne -o grammar.js
    ```
3. Test the grammar using one of the given **acceptedExample1-4.txt**:
    ```
   $ nearley-test -i cat acceptedExample1.txt grammar.js
   ```
   nearley returns the result of his parsing of the document following the given grammar.