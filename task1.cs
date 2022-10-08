using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace syntactic_tree_v2
{
    class Program
    {
        #region PRIVATE ATTRIBUTES

        // Syntactic Tree: is the output the program has ti build.
        static private string[][] syntacticTree;

        // Final message that tells if the input is a formula in propositional logic or not.
        static private string finalMessage;

        #endregion PRIVATE ATTRIBUTES

        #region MAIN

        static void Main(string[] args)
        {
            // Inputs for testing.
            string input = "((p && q) || (¬p || ¬q))";
            input = "((p -> q) || (p -> r))";
            input = "(p -> ((q || p) -> r))";
            input = "(((p -> ¬r) && ¬¬(p || r)) <-> (p && ¬q))";
            input = "(((p -> ¬r) && ¬¬( || r)) <-> (p && ¬q))";
            input = "((p -> ¬r) && ¬(¬(p || r) <-> (pp && ¬q)))";
            //input = "((¬q || (p -> ¬r)) <-> (¬((p222&&) && q))";
            //input = "p123";
            //input = "(p)";
            //input = "((p -> q) || (p  r))";
            //input = "()( && q)";

            // Preprocessing the input expression.
            input = PreProcessingData(input);

            // Variable to indicate if some bad expression is founded during the analysis.
            bool badExpressionFounded = false;

            // Variable to store which level of the syntactic tree we are working on.
            int level = 1;

            // Number of the atomic sentence we find in the input.
            int numberAtomicSentences = NumberAtomicSentences(input);

            // Initialize the syntactic tree with as many rows as atomic sentences we found in the input.
            syntacticTree = new string[numberAtomicSentences][];

            // In any row of the atomic sentence, we initialize a new array with the input.
            for (int i = 0; i < syntacticTree.Length; i++)
                syntacticTree[i] = new string[] { input };

            // We start the loop, until we find a bad expression, or until the analysis is finished (see the function IsFinished()).
            while (!badExpressionFounded)
            {
                // Get the expressions of the last level filled in the syntactic tree.
                string[] expressions = GetFormulasLastLevel(level - 1);

                // We check if the formulas founded in the last level are all of them Atomic Sentences. If so, we exit the loop.
                if (IsFinished())
                    break;

                // We add a new level to include the subformulas we find in the last level's formulas.
                level += 1;

                // Loop to analyze every expression of the array with the formulas of the last level.
                for (int i = 0; i < expressions.Length; i++)
                {
                    // Get the subformulas of the current expression.
                    string[] subExpressions = GetSubFormulas(expressions[i]);

                    // If the array with the subformulas is null, it means that we found a bad expression.
                    if (subExpressions == null)
                    {
                        // Variable badExpressionFounded gets true.
                        badExpressionFounded = true;

                        // The final message will say that we found a bad expression, so we stop the analysis.
                        finalMessage = string.Format("The expression {0} is not a Formula in Propositional Logics.{1}The Syntactic Tree was aborted.", OutputData(expressions[i]), Environment.NewLine);
                        
                        // Exit the loop.
                        break;
                    }

                    // Loop to fill the syntactic tree with every subformula founded.
                    for (int j = 0; j < subExpressions.Length; j++)
                        FillSyntacticTree(subExpressions[j], level);
                }
            }

            // Print the result in the console.
            PrintResult();
        }

        #endregion MAIN

        #region BASIC FUNCTIONS

        /// <summary>
        /// Indicates if the character is a Lower Letter.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if it is a letter.</returns>
        private static bool IsLowerLetter(char character) => character >= 97 && character <= 122;

        /// <summary>
        /// Indicates if the character is a Number from 0 to 9.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if it is a number.</returns>
        private static bool IsNumber(char character) => character >= 48 && character <= 57;

        /// <summary>
        /// Indicates if the character is a negation in propositional logic.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if is a Negation.</returns>
        private static bool IsNegation(char character) => character == '¬';

        /// <summary>
        /// Indicates if the character is a opening bracket.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if it is a opening bracket.</returns>
        private static bool IsOpeningBracket(char character) => character == '(';

        /// <summary>
        /// Indicates if the character is a opening bracket.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if it is a opening bracket.</returns>
        private static bool IsClosingBracket(char character) => character == ')';

        /// <summary>
        /// Indicates if the character is a propositional logic connector.
        /// </summary>
        /// <param name="character">character to be analyzed.</param>
        /// <returns>True if is a connector.</returns>        
        private static bool IsConnector(char character) => character == '|' || character == '&' || character == '-' || character == '+';

        #endregion BASIC FUNCTIONS

        #region I/O FUNCTIONS
        
        /// <summary>
        /// Get the white spaces out.
        /// </summary>
        /// <param name="input">Input introduced by the user.</param>
        /// <returns>Expression with no blank spaces, and with connectors just occupying one digit.</returns>
        private static string PreProcessingData(string input)
        {
            return input.Replace(" ", "").Replace("<->", "+").Replace("->", "-").Replace("||", "|").Replace("&&", "&");
        }

        /// <summary>
        /// Change the connectors to the original ones.
        /// </summary>
        /// <param name="expression">Expression that you want to transform.</param>
        /// <returns>New Expression.</returns>
        private static string OutputData(string expression)
        {
            return expression.Replace("-", "->").Replace("+", "<->").Replace("|", "||").Replace("&", "&&");
        }

        /// <summary>
        /// PRint the output in the console.
        /// </summary>
        private static void PrintResult()
        {
            // Loop in the roads of the syntactic tree.
            for (int i = 0; i < syntacticTree.Length; i++)
            {
                // Loop in the different levels of a road.
                for (int j = 0; j < syntacticTree[i].Length; j++)
                {
                    // If the cell of the syntactic tree is null, it means there was some problem on the analysis, so we exit the loop.
                    if (syntacticTree[i][j] == null)
                        break;

                    // Print the value of the cell, and tab.
                    Console.Write(OutputData(syntacticTree[i][j]) + "\t");
                }

                // New Line in the console.
                Console.WriteLine();
            }

            // New line in the console.
            Console.WriteLine();

            // Print the final message, or a generic message if the final message is null.
            Console.WriteLine(finalMessage ?? "BAD FORMAT");

            // Wait for the user.
            Console.ReadLine();
        }

        #endregion I/O FUNCTIONS

        #region ATOMIC SENTENCES FUNCTIONS

        /// <summary>
        /// Check if the Sentence is an atomic sentence.
        /// </summary>
        /// <param name="expression">Expression to be analyzed.</param>
        /// <returns>Treu if is an atomic sentence.</returns>
        private static bool IsAtomicSentence(string expression)
        {
            // Number of lower letters founded.
            int numberOfLoweLetters = 0;

            // Number of Bad Characters.
            int badCharacters = 0;

            // Loop in the expression to read the characters.
            for (int i = 0; i < expression.Length; i++)
            {
                // We store the current char.
                char c = expression[i];

                // If the char is not a lower letter or a number, we add 1 to the number of bad characters.
                if (!(IsLowerLetter(c) || IsNumber(c)))
                    badCharacters = badCharacters + 1;

                // If the character is a lower letter, we add 1 to the number of lower letters founded.
                else if (IsLowerLetter(c))
                    numberOfLoweLetters += 1;
            }

            // f = First character of the expression is a letter.
            bool f = IsLowerLetter(expression[0]);

            // m = There is more than one letter.
            bool m = numberOfLoweLetters > 1;

            // b = Has some Bad Character.
            bool b = badCharacters > 0;

            // Sufficient conditions for the expression to be an atomic sentence.
            return f && !m && !b;
        }

        /// <summary>
        /// Number of the atomic sentences inside of an expression.
        /// </summary>
        /// <param name="expression">Expression to be analyzed.</param>
        /// <returns>Number of atomic sentences.</returns>
        static private int NumberAtomicSentences(string expression)
        {
            // Variable to store the number of Atomic Sentences founded.
            int numberAtomicSenteces = 0;

            // Loop to read the different charaters of the exoression.
            for (int i = 0; i < expression.Length; i++)
            {
                // We store the current character.
                char c = expression[i];

                // If the character is a lower letter, we add one to the number of atomic sentences founded.
                if (IsLowerLetter(c))
                    numberAtomicSenteces += 1;
            }

            // Return the number of atomic sentences founded.
            return numberAtomicSenteces;
        }

        #endregion ATOMIC SENTENCES FUNCTIONS

        #region FORMULAS ANALYSIS

        /// <summary>
        /// Get the Formulas of the Last Level to Analyze.
        /// </summary>
        /// <param name="level">Level of the Syntactic Tree.</param>
        /// <returns>Number of SubFormulas Founded.</returns>
        private static string[] GetFormulasLastLevel(int level)
        {
            // Variable to count the number of expressions we find in the last level.
            int numberExpressions = 0;

            // Variable to store the expressions we find in the different rows.
            string expression = string.Empty;

            // Loop to include the non repetaed expressions.
            for (int i = 0; i < syntacticTree.Length; i++)
            {
                // If the expression read in the syntactic tree is different to the last one we read, we add one to the number of expressions.
                if (syntacticTree[i][level] != expression)
                    numberExpressions += 1;

                // We store the new value founded in the variable expression.
                expression = syntacticTree[i][level];
            }

            // Index of the expression.
            int indexExpression = 1;

            // Array to include the expressions founded in the last level.
            string[] expressions = new string[numberExpressions];

            // We add the first expression in the array.
            expressions[0] = syntacticTree[0][level];

            // Loop to read the rest of expressions.
            for (int i = 1; i < syntacticTree.Length; i++)
            {
                // If the expression read is different than the last one, we add it into the array.
                if (syntacticTree[i][level] != syntacticTree[i - 1][level])
                    expressions[indexExpression++] = syntacticTree[i][level];
            }

            // We return the array with the expressions founded.
            return expressions;
        }

        /// <summary>
        /// Get the Subformulas included in the input.
        /// </summary>
        /// <param name="expression">Expression to find the subformulas.</param>
        /// <returns>Array with the subformulas founded. Null means that the expression is not a formula.</returns>
        private static string[] GetSubFormulas(string expression)
        {
            // If the expression is null or empty, we return null.
            if (string.IsNullOrEmpty(expression))
            {
                return null;
            }

            // If the expression is an atomic sentences, we give back the same formula.
            else if (IsAtomicSentence(expression))
            {
                return new string[] { expression };
            }

            // If the expression is a negation, we return the sentence after the negation.
            else if (IsNegation(expression[0]))
            {
                return new string[] { expression.Substring(1) };
            }

            // In any other case...
            else
            {
                // We read the first and the last characters of the expression.
                char firstCharacter = expression[0];
                char lastCharacter = expression[expression.Length - 1];

                // If the expression has not opening and closing brackets, is not a formula, so we return null.
                if (!(IsOpeningBracket(firstCharacter) && IsClosingBracket(lastCharacter)))
                {
                    return null;
                }
                else
                {
                    // We find the position of the string for the main connector.
                    int positionMainConnector = PositionMainConnector(expression);

                    // If we don't find any connector, is not a formula, so we return null.
                    if (!(positionMainConnector != 0))
                        return null;

                    // We read the expression before the connector.
                    string leftExpression = expression.Substring(1, positionMainConnector - 1);

                    // We read the expression after the connector.
                    string rightExpression = expression.Substring(positionMainConnector + 1, expression.Length - positionMainConnector - 2);

                    // If the left expression or right expression is empty/null, the expression is not a formula.
                    if (string.IsNullOrEmpty(leftExpression) || string.IsNullOrEmpty(rightExpression) || NumberAtomicSentences(leftExpression) <= 0 || NumberAtomicSentences(rightExpression) <= 0)
                        return null;

                    // We return the array including the subformulas founded.
                    return new string[] { leftExpression, rightExpression };
                }
            }
        }

        /// <summary>
        /// Find the position of the main connector into the input.
        /// </summary>
        /// <param name="expression">Expression to be analyzed.</param>
        /// <returns>Position of the main connector. If 0 means that we didn't find it.</returns>
        private static int PositionMainConnector(string expression)
        {
            // Variable to store the position of the main connector. 0 if not founded.
            int positionMainConnector = 0;

            // Number of Brackets read.
            int numberOfBrackets = 0;

            // Loop to read the characters of the expression.
            for (int i = 0; i < expression.Length; i++)
            {
                // We store the current character.
                char c = expression[i];

                // If the character is an opening bracket, we add 1 to the number of brackets.
                if (IsOpeningBracket(c))
                {
                    numberOfBrackets += 1;
                }

                // If bracket is a closing bracket, we sustract 1 to the number of brackets.
                else if (IsClosingBracket(c))
                {
                    numberOfBrackets -= 1;
                }

                // If the character is a connector, and the number of brackets is 1, we already found the main connector.
                else if (IsConnector(c) && numberOfBrackets == 1)
                {
                    // We store the position of the main connector.
                    positionMainConnector = i;

                    // Exit the loop. We already finish.
                    break;
                }
            }

            // We return the value.
            return positionMainConnector;
        }

        #endregion FORMULAS ANALYSIS

        #region SYNTACTIC TREE

        /// <summary>
        /// Indicates if the analysis is finished (i. e. if all the formulas of the last level are atomic sentences).
        /// </summary>
        /// <returns>True if all the formulas of the last level are atomic sentences.</returns>
        private static bool IsFinished()
        {
            // Last level of the Syntactic Tree.
            int lastLevel = syntacticTree[0].Length - 1;

            // We read all the values of the last level.
            for (int i = 0; i < syntacticTree.Length; i++)
            {
                // Expression of the last level for this row.
                string expression = syntacticTree[i][lastLevel];

                // If the expression is null, or is not an atomic sentence, that is a sufficient condition to know that the analysis is not finished.
                if (expression == null || !IsAtomicSentence(expression))
                    return false;
            }

            // If the formula is OK, we say that in the final message and return true.
            finalMessage = "The sentence is a Propositional Logic Formula";
            return true;
        }

        /// <summary>
        /// Fill the syntactic Tree with a new Expression.
        /// </summary>
        /// <param name="expression">Expression that we have to add.</param>
        /// <param name="level">Level of the syntactic tree where we have to include the expression.</param>
        private static void FillSyntacticTree(string expression, int level)
        {
            // If is the first formula of this new level, we have to add another level to the syntactic tree.
            if (level > syntacticTree[0].Length)
            {
                // Loop to include a new level in all the syntactic tree rows.
                for (int i = 0; i < syntacticTree.Length; i++)
                {
                    // Saved Data is a Backup of the data stored in the current row of the syntactic Tree until now.
                    string[] savedData = syntacticTree[i];

                    // We create a new array adding one level.
                    syntacticTree[i] = new string[syntacticTree[i].Length + 1];

                    // Then we recover the data saved in the new array of the syntactic Tree.
                    for (int j = 0; j < savedData.Length; j++)
                        syntacticTree[i][j] = savedData[j];
                }
            }

            // Number of atomic sentences of the expression.
            int numberOfAtomicSentences = NumberAtomicSentences(expression);

            // Loop of the last level of the rows to include the expression in the proper rows.
            for (int i = 0; i < syntacticTree.Length; i++)
            {
                // if the row has already a value, we skip it.
                if (syntacticTree[i][syntacticTree[i].Length - 1] != null)
                    continue;

                // if we find an empty row, we add the expression in as many rows as number of atomic sentences the expression has.
                for (int j = 0; j < numberOfAtomicSentences; j++)
                    syntacticTree[i + j][syntacticTree[i].Length - 1] = expression;
                
                // We exit the loop.
                break;
            }
        }

        #endregion SYNTACTIC TREE
    }
}
