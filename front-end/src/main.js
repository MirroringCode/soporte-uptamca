import { swapTheme } from "./utils/swapTheme";
import { checkAllTable } from "./utils/checkboxAllTable";

const elements = {
   themeSwap: document.getElementById('themeSwap'),
   calledFunctions: {
    checkAllTable: checkAllTable(document.querySelector('.table')),
   }
}

elements.themeSwap.addEventListener('change', () => {
    swapTheme();
});


