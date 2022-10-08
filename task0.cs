using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Task_0
{
    class Program
    {
        static void Main(string[] args)
        {
            string input = "(((p-> ¬r) && ¬¬(p || r)) <-> (p && ¬q))";
            //input = "(p&&q)";
            //input = "((p || q) && ¬(p && q))";
            //input = "¬¬¬¬¬p";
            //input = "¬¬(¬¬(p && ¬q))";
            //input = "((p-> ¬r) && ¬¬(p || r)) <-> (p && ¬q)";
            //input = "p && q";
            //input = "(p)"; FALLA
            //input = "(p -> q) || (p -> r)";
            input = "p -> ((q || p) -> r)";
            input = "(p -> ¬r) && ¬(¬(p || r) <-> (p && ¬ q))";
            input = "(p -> ¬r) && ¬(¬(p || R) <-> (p && ¬ q))";
            //input = "p454";

            //input = "p123";
            //input = "123";

            input = PreProcessingData(input);

            if (CheckSufficientConditions(input))
                Console.WriteLine("The Sentence is ok");
            else if (!CheckNecessaryConditions(input))
                Console.WriteLine("The Sentence is NOT ok");
            else 
                Console.WriteLine("I don't know if the sentence is OK");

            Console.ReadLine();
        }

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
        /// Check the Sufficient Conditions to figure out if the input is a Formula in Propositional Logic.
        /// </summary>
        /// <param name="expression">Pre-processed input.</param>
        /// <returns>True if is an Atomic Sentence.</returns>
        private static bool CheckSufficientConditions(string expression)
        {
            return IsAtomicSentence(expression);
        }

        /// <summary>
        /// Check some basic necessaty conditions.
        /// </summary>
        /// <param name="expression">Expression to be analyzed.</param>
        private static bool CheckNecessaryConditions(string expression)
        {
            int startBrackets = 0;
            int endBrackets = 0;
            int badCharacter = 0;

            // Atomic Sentence that indicates if in some moment we have more closing than opening brackets.
            bool m = false;

            for (int i = 0; i < expression.Length; i++)
            {
                char c = expression[i];

                // First-order logic would be better here...
                if (!IsLowerLetter(c) && !IsNumber(c) && !IsBracket(c) && !IsConnector(expression[i]))
                    badCharacter += 1;
                else if (IsOpeningBracket(c))
                    startBrackets += 1;
                else if (IsClosingBracket(c))
                    endBrackets += 1;

                if (startBrackets < endBrackets)
                {
                    m = true;
                    break;
                }
            }

            // s = Same Number of Parenthesis.
            bool s = startBrackets == endBrackets;

            // b = There is one bad character.
            bool b = badCharacter > 0;

            return s && !b && !m;
        }

        /// <summary>
        /// Check if the Sentence is an atomic sentence.
        /// </summary>
        /// <param name="expression">Expression to be analyzed.</param>
        /// <returns>Treu if is an atomic sentence.</returns>
        private static bool IsAtomicSentence(string expression)
        {
            int numberOfLetters = 0;
            int badCharacters = 0;

            // First-order logic would be better here...
            for (int i = 0; i < expression.Length; i++)
            {
                char c = expression[i];
                if (!(IsLowerLetter(c) || IsNumber(c)))
                    badCharacters = badCharacters + 1;
                else if (IsLowerLetter(c))
                    numberOfLetters += 1;
            }

            // f = First character of the expression is a letter.
            bool f = IsLowerLetter(expression[0]);

            // m = There is more than one letter.
            bool m = numberOfLetters > 1;

            // b = Has some Bad Character.
            bool b = badCharacters > 0;

            return f && !m && !b;
        }

        /// <summary>
        /// Indicates if the character is a propositional logic connector.
        /// </summary>
        /// <param name="character">character to be analyzed.</param>
        /// <returns>True if is a connector.</returns>        
        private static bool IsConnector(char character) => character == '|' || character == '&' || character == '-' || character == '+' || IsNegation(character);

        /// <summary>
        /// Indicates if the character is a negation in propositional logic.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if is a Negation.</returns>
        private static bool IsNegation(char character) => character == '¬';

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
        /// Indicates if the character is a bracket.
        /// </summary>
        /// <param name="character">Character to be analyzed.</param>
        /// <returns>True if it is a bracket.</returns>
        private static bool IsBracket(char character) => IsOpeningBracket(character) || IsClosingBracket(character);
    }
}
