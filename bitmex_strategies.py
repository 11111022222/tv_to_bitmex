import bitmex_redemption.bitmex_redemption_strategy as redemption_strategy #à remplacer par votre script qui executera la strategie
REDEMPTION_STRATEGY_LONG = "long_redemption"
REDEMPTION_STRATEGY_STOPLONG = "stop_long_redemption"
REDEMPTION_STRATEGY_SHORT = "short_redemption"
REDEMPTION_STRATEGY_STOPSHORT = "stop_short_redemption"
def call_strategy(email_snippet):
#calling redemption strategy
    if REDEMPTION_STRATEGY_STOPLONG in email_snippet:
        redemption_strategy.stop_long()
    elif REDEMPTION_STRATEGY_LONG in email_snippet:
        redemption_strategy.long()
    elif REDEMPTION_STRATEGY_SHORT in email_snippet:
        redemption_strategy.short()
    elif REDEMPTION_STRATEGY_STOPSHORT in email_snippet:
        redemption_strategy.stop_short()
