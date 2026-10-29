# Playbook replay: the terminal-break record

Generated 2026-10-29T22:53:02+00:00 by `evals/live_book/playbook_replay.py`, prompt `v3.3`, narrator `gpt-5.4-mini`, API cost at most $0.32.

Every archived live-run leg whose diagnostic pass ended in a terminal break (36 legs) was replayed twice on the same code: playbook off and on. Only the narrator is a real model; the digester and the critic return their archived answers and the verifier is off, so the arms differ by the record alone. 35 legs are still terminal breaks under the current code and are scored.

A verdict "flags the break" if it uses any of the words *unexplained*, *not explain*, *unattributed*, *human review* or *not reliable*. That broad match also counts a verdict that names the break only to play it down ("the small unexplained break is consistent with higher-order effects") or that calls the quote unreliable. The strict row counts only "does not explain" (or "does not fully explain") and "human review".

| | Playbook off | Playbook on |
|---|---|---|
| Verdict flags the break (broad) | 10/35 | 35/35 |
| Verdict says the move is not explained or needs human review (strict) | 0/35 | 35/35 |
| Confidence rationale flags the break | 29/35 | 34/35 |
| Narrator fell back to the rule-based summary | 0/35 | 0/35 |

## What this does not show

- The verifier is off, so this is the narrator's verdict after the deterministic reconcile step. With the verifier on, a PARTIAL adds a caveat to the verdict and a FAIL that code confirms replaces it.
- One model, one run per leg.
- Whether the record crowds out a catalyst. Only one of these legs had headline mechanisms, under an observation lock that tells the narrator not to force a catalyst, and neither arm named it. The offline test on VW 2008 (`tests/agent/test_playbook.py`) checks the prompt, not a real model.

## Verdicts, leg by leg

### 2026-09-07/live_174215/legs/AAPL.json

- **Off**: The move is explained first by the modeled delta exposure, with the call revaluing lower as the underlying sold off. Gamma and implied volatility provided some offset, while theta added to the drag; the remaining gap is a small method residual consistent with higher-order effects in a fast spot move. There is no headline catalyst layer to add here, and the observation lock means the run should be treated as a model-driven attribution rather than a news-led one.
- **On** (flags it): The dominant modeled driver is the spot decline passing through a high-delta call, with theta also pressuring the mark and only minor offset from convexity and volatility. However, the attribution does not fully explain this move and the diagnostic pass flags a terminal break, so the story needs human review rather than a single-factor conclusion.

### 2026-09-07/live_174215/legs/GOOGL.json

- **Off**: The move is explained first by the modeled sensitivity to implied volatility, with the spot decline playing a secondary offsetting role and gamma plus theta contributing smaller effects. Because the observation is locked and no relevant headlines were retrieved, there is no independent catalyst layer to add; the run is a model attribution of the full revaluation rather than a news-driven explanation.
- **On** (flags it): The modeled move is led by a vega revaluation, with the larger implied-volatility reset dominating the Taylor view while spot and time decay partly offset it. That said, the attribution does not explain this move cleanly: the residual is still material, the observation is unreliable, and the story needs human review rather than a single-factor conclusion. There are no relevant headlines in the digest, so no external catalyst mechanism is confirmed here.

### 2026-09-07/live_174215/legs/KO.json

- **Off**: The move is explained first by the option’s high sensitivity to the underlying, with a smaller contribution from time decay. The residual is modest, so the run is largely a clean full revaluation of the same engine rather than a separate event-driven repricing. Early exercise is economically relevant here because the dividend cover is material relative to remaining time value, so the American feature still matters in the valuation path.
- **On** (flags it): The modeled move is led by delta, with the call losing value as the shares slipped and time decay adding to the downside. That said, the attribution does not explain the full move and the run needs human review; the residual and terminal break mean the Greek story is only a partial account of the revaluation. The American setup is materially relevant because the dividend/exercise boundary is part of the pricing context, but there are no retrieved headlines to supply an additional catalyst.

### 2026-09-07/live_174215/legs/META.json

- **Off**: The move is a carry-dominated revaluation: time decay overwhelmed the positive spot and volatility contributions, leaving the option’s model price essentially unchanged on the day despite the underlying rally. The residual is consistent with higher-order option curvature and path effects around a short-dated American contract, but there is no retrieved headline catalyst to assign as a separate Layer B driver. 
- **On** (flags it): The modeled move is led by carry and time decay, with spot and volatility contributing only secondary support in the Taylor view. However, the attribution does not explain this move cleanly: a meaningful portion remains unexplained and the diagnostic pass flags a terminal break, so the story needs human review rather than a full single-factor explanation.

### 2026-09-07/live_174215/legs/MSFT.json

- **Off**: The position’s close-to-close move is explained first by delta exposure to the lower spot, with gamma helping cushion part of that move while theta and the small implied-vol dip offset some of the gain. The remaining gap is a higher-order model residual, which is consistent with a truncated Taylor view on a named put under a sharp underlying move rather than a separate news catalyst. Early exercise is not a meaningful factor here because the dividend does not justify immediate exercise at current marks.
- **On** (flags it): The modeled attribution is led by delta, but the pass does not explain this move cleanly and a meaningful portion remains unexplained, so the story needs human review. The spot slide and modest implied-vol drift support the direction of the option revaluation, while the residual indicates higher-order effects and path dependence that the Taylor bucket did not capture. No named headline catalyst was available, so there is no confirmed Layer B event to anchor the gap story.

### 2026-09-07/live_174215/legs/NVDA.json

- **Off**: The move is a carry-dominated theta case: the option’s time decay outweighed the modest spot drift and the small implied-vol uptick, leaving the full revaluation essentially flat. The remaining gap is best read as model noise and higher-order effects under a short-dated American option, not as a fresh catalyst story, since no relevant headlines were retrieved and the observation is locked.
- **On** (flags it): The modeled close-to-close move is led by time decay, with spot and implied volatility offsetting part of the carry loss. However, the attribution does not explain this move cleanly: a terminal unexplained break remains, so the story needs human review rather than a fully closed Greek explanation.

### 2026-09-07/live_174215/legs/SPY.json

- **Off** (flags it): The modeled move is dominated by a higher implied-volatility mark on the put, with delta and gamma from the small spot dip adding only a secondary lift and theta offsetting part of that change. Because the observation is locked and no relevant headlines were retrieved, there is no named catalyst layer to attach; the remaining model gap is best treated as an unexplained residual inside the revaluation rather than a news-driven story.
- **On** (flags it): The blotter’s modeled driver is vega, with spot and theta also contributing in offsetting ways, but the attribution does not fully explain this move. A large unexplained break remains, so this run should be treated as a partial model explanation rather than a complete causal read; human review is needed. There are no retrieved headlines or named tape mechanisms to add a Layer B catalyst, so no external event can be confirmed from the record.

### 2026-09-07/live_174215/legs/TSLA.json

- **Off**: The option move is dominated by the underlying selloff, with the call repricing lower as spot fell through the strike area and delta carried most of the model change. Gamma and vega offset part of that move, but the tape still reads as a straightforward spot-driven revaluation rather than a fresh event-led repricing. The residual is small, so higher-order effects are present but not the main story; the relevant Tesla headlines are background context rather than a separate mechanism.
- **On** (flags it): The modeled move is dominated by spot sensitivity, with the option revaluing lower as the underlying fell sharply and the call lost intrinsic support. That said, the attribution does not explain this move in full; the terminal break means the remaining gap needs human review rather than a single-factor story. The relevant Tesla headlines provide context on stock sentiment and product/regulatory risk, but they are not enough to replace the model story or fully account for the unexplained portion.

### 2026-09-14/live_223505/legs/AAPL.json

- **Off**: The move is explained primarily by the option’s positive delta responding to the modest rise in the underlying, with gamma adding only a small convexity support and theta decay offsetting much of that gain. The residual is consistent with higher-order path effects and model truncation around a tight close-to-close revaluation, but there is no headline catalyst to assign the gap to and no early-exercise feature standing out in the mark.
- **On** (flags it): The modeled attribution is led by delta, with a smaller offset from theta and a mild drag from the implied-vol move. That said, the attribution does not fully explain this move and the diagnostic pass flags a terminal unexplained break, so the story needs human review rather than a single-factor conclusion.

### 2026-09-14/live_223505/legs/JPM.json

- **Off** (flags it): The position’s modeled move was led by a sharp drop in implied volatility, with spot also lower and theta decay adding to the headwind. The full revaluation ended flat because the run is dominated by offsetting factors and a large unexplained break, so the Taylor view should be treated as a reference rather than a complete explanation. There are no relevant retrieved headlines, so no auxiliary catalyst story can be assigned beyond the observed volatility reset.
- **On** (flags it): The blotter’s modeled factor split points to implied-volatility compression as the dominant attribution, but the overall move is not cleanly explained by the Greek decomposition. A meaningful unexplained break remains, so the attribution does not fully account for the price change and needs human review rather than a single-factor explanation.

### 2026-09-14/live_223505/legs/KO.json

- **Off**: The option’s price change is explained first by a delta-led revaluation as the stock firmed into a deep in-the-money call profile. Gamma added a small convexity boost while theta worked against the move, and the remaining gap is consistent with model truncation rather than a separate catalyst. No relevant headlines were retrieved, so there is no supported Layer B news mechanism to add beyond the model move; the early-exercise setup remains relevant because the dividend coverage makes exercise economics meaningful.
- **On** (flags it): The attribution is led by spot-sensitive delta, with gamma supporting the move and theta partly offsetting it. That said, the diagnostic pass does not explain this move fully: the residual is still present, and the engine has flagged a terminal break, so the story needs human review rather than a single-factor conclusion. Early exercise is economically relevant here, so the American contract is being shaped by dividend and exercise dynamics inside the model.

### 2026-09-14/live_223505/legs/META.json

- **Off**: The move is best explained by the modeled delta exposure: the rally in the underlying was the main offsetting force against time decay and the implied-volatility drop. The Taylor view also shows convexity helping on the up move, but the large vol reset and theta bleed pulled against that gain, leaving a near-flat full revaluation in the engine. No named catalyst was retrieved, so the tape is a model-driven attribution rather than a news-led one.
- **On** (flags it): The modeled attribution points first to delta on the underlying move, with gamma and theta as secondary contributors and a concurrent vega drag from the implied-volatility reset. The attribution does not explain this move in full: the terminal break leaves a meaningful unexplained remainder, so the tape needs human review rather than a single-cause story. There are no relevant headlines to attach as a catalyst layer, and the available evidence does not support inventing a news-driven mechanism.

### 2026-09-14/live_223505/legs/MSFT.json

- **Off**: The run is dominated by a revaluation tied to the move in implied volatility, while the spot rise and theta also offset the option’s value through the day. Because observation is locked and the residual is large, the headline attribution should be read as a model decomposition with meaningful higher-order or path-dependent noise rather than a clean single-factor story.
- **On** (flags it): The attribution is dominated by implied-volatility revaluation, but the diagnostic pass does not fully explain the move and needs human review. The large unexplained break means the Greek decomposition is only a partial account here; with no retrieved headlines and observation locked, there is no confirmed catalyst layer to name as the cause.

### 2026-09-14/live_223505/legs/NVDA.json

- **Off**: The position moved mainly on the underlying selloff, with the option price dominated by delta exposure while gamma partially cushioned the decline. The small residual is consistent with normal second-order and path effects in a short-dated American call, and the early-exercise premium is not a factor. The headlines provide only sector background — broad chip and AI-related weakness fits the direction of the move, but there is no company-specific catalyst or control-structure event to add as a separate mechanism.
- **On** (flags it): The position was dominated by delta exposure, with the lower spot level driving the model revaluation and the second-order terms only cushioning part of the move. The attribution does not fully explain this move, so the break needs human review rather than a single-cause explanation. The kept headlines are only broad chip-and-tech sentiment in the background and do not establish a company-specific catalyst.

### 2026-09-14/live_223505/legs/SPY.json

- **Off**: The position’s modeled move was led by time decay, with spot and implied volatility contributing in the same direction but not overcoming the passage of time. Because the residual is elevated and the spot move was small, the remaining gap is most consistent with higher-order effects and American exercise boundary shifts rather than a clean single-factor explanation. The option also sits in an economically relevant early-exercise setup, so the dividend schedule is part of the pricing context even though the early-exercise premium itself is small.
- **On** (flags it): The modeled attribution points first to theta decay as the dominant engine of the 1-day change, with spot and implied volatility both contributing smaller offsetting effects. However, the attribution does not explain this move: a meaningful part of the revaluation remains unexplained, so the tape needs human review rather than a single-factor story. The American exercise setup is relevant only as a boundary condition here; it does not fully account for the break.

### 2026-09-14/live_223505/legs/TSLA.json

- **Off**: The move is explained first by the position’s delta exposure to the lower spot close, with gamma partly softening the decline and theta a smaller drag. The sharp implied-volatility jump offset much of the spot effect, so the option’s model value finished essentially unchanged even though the tape was clearly active.
- **On** (flags it): The attribution is led by Delta, with the lower spot close pressuring the call while Vega partly offset that effect and Gamma provided some cushioning. However, the attribution does not explain this move cleanly: a large terminal break remains, so the story needs human review rather than a single-factor explanation. The relevant Tesla headline about a new Roadster unveiling fits the tape as company-specific context, but it is not confirmed as the cause of the unexplained remainder.

### 2026-09-14/live_223505/legs/XOM.json

- **Off** (flags it): The modeled move is led by the put’s negative delta against the small spot decline, with gamma providing only a minor offset and theta plus vega working against the position. Because observation is unreliable and the headline set is empty, the run should be read as a clean model revaluation with a terminal unexplained break rather than a news-driven dislocation.
- **On** (flags it): The modeled move is led by delta, with the spot slip and the option’s negative delta producing the main direction of the revaluation. Vega and theta also offset the tape, but the attribution does not explain this move cleanly; the terminal break flag means a meaningful part of the change remains unexplained and needs human review.

### 2026-09-21/live_210040/legs/JPM.json

- **Off** (flags it): The move is primarily a time-decay revaluation in the official engine, with the option losing value as expiry approached despite only a modest spot change. Vega also contributed to the decline, but the desk’s suppressed-vol narrative should stay secondary here because observation quality is poor and the diagnostic flags limit a fuller catalyst read. The remaining unexplained break is consistent with higher-order model effects and path dependency around the short-dated American structure rather than a separate news catalyst.
- **On** (flags it): The blotter’s modeled move is led by time decay, with additional pressure from the implied volatility drop and a small spot drift in the unfavorable direction for the put. However, the attribution does not explain this move cleanly: a material portion of the model change remains unexplained, so the story needs human review rather than a single-factor conclusion.

### 2026-09-21/live_210040/legs/KO.json

- **Off**: The move is primarily explained by a revaluation from higher implied volatility, with spot contributing positively and theta partially offsetting the gain. The residual is sizable, so the close-to-close Taylor view should be read as a reference rather than a complete explanation, but there is no retrieved headline catalyst to assign as a separate mechanism.
- **On** (flags it): The dominant modeled driver is vega, with the option’s mark rising mainly as implied volatility moved higher; delta also helped, while theta offset part of the gain. That said, the attribution does not explain this move in full: the residual is large and the diagnostic pass is flagged as a terminal break, so the story needs human review rather than a single-factor explanation.

### 2026-09-22/live_210038/legs/JPM.json

- **Off**: The modeled move is led by delta: the option marked against a higher JPM spot print, which pushed the put against the position. That was partially offset by a sharp implied-volatility jump that supported option value, while theta was a smaller drag and gamma only a minor contributor. The residual remains notable because the move was large relative to the short-dated setup and the engine flags a terminal break, so the full revaluation is the cleaner read than the Taylor split alone.
- **On** (flags it): The modeled move is led by delta, with the option gaining exposure from the higher close in the underlying while gamma and theta are secondary effects. That said, the attribution does not explain this move cleanly: the residual is still large, so the story needs human review rather than a fully closed Greek explanation. The relevant JPMorgan headlines provide background around the tape, but they are not confirmed as the cause of the model gap.

### 2026-09-22/live_210038/legs/KO.json

- **Off**: The move was driven primarily by the underlying drifting lower, which hit the call’s directional exposure and outweighed the positive contribution from volatility. The residual is modest relative to the modeled change and is consistent with higher-order truncation and path effects rather than a separate catalyst. With no retrieved headlines and observation locked, there is no supported Layer B event story to add beyond the factor decomposition.
- **On** (flags it): The modeled move is led by delta, with the stock trading lower and the call losing directional value, while gamma and theta partially offset and vega adds support from the volatility reset. However, the attribution does not fully explain this move and the story needs human review; the unexplained break means the remaining gap should be treated as unresolved rather than assigned to a catalyst.

### 2026-09-22/live_210038/legs/XOM.json

- **Off** (flags it): The move is dominated by the put’s directional sensitivity to the decline in the underlying, with gamma reinforcing the convex payoff as spot moved lower. A separate implied-volatility rise also supported the revaluation, but the desk signal suppresses a Vega narrative and there are no relevant headlines to anchor a catalyst story. The small unexplained break is consistent with higher-order model effects and path revaluation noise rather than a separate event-driven mechanism.
- **On** (flags it): The attribution is led by the position’s directional sensitivity, with the spot drop driving the modeled revaluation and gamma and implied volatility acting as secondary supports. However, the diagnostic pass does not fully explain this move; a terminal break remains and the story needs human review rather than a single-factor conclusion. The early-exercise premium is negligible, so American exercise is not the source of the discrepancy.

### 2026-09-23/live_210024/legs/XOM.json

- **Off** (flags it): The revaluation is dominated by the put’s directional response to the underlying decline, with the option gaining as spot moved lower from the prior close. That said, the move also came alongside an unusually large implied-volatility reset, so the full revaluation reflects both the spot effect and a volatility-related reprice rather than a clean single-factor day. The remaining unexplained break is consistent with higher-order model effects and quote noise under a short-dated, high-vol regime.
- **On** (flags it): The modeled move is led by delta, with the put benefiting from the decline in the underlying and gamma providing a smaller convexity lift. However, the attribution does not explain this move cleanly: a large unexplained break remains, so the story needs human review rather than a single-factor conclusion.

### 2026-09-24/live_210022/legs/JPM.json

- **Off** (flags it): The move is explained first by the put’s directional sensitivity to the lower spot close, with the full revaluation still showing the position benefited mainly from the downside spot move. The volatility jump is part of the model revaluation, but the diagnostic setup suppresses a Vega narrative here because the observation is unreliable and no relevant headline catalyst was retrieved. The unexplained break remains large enough to flag higher-order model effects or mark noise, so the attributed move should be treated as a model explanation rather than a news-driven event.
- **On** (flags it): The modeled move is led by spot sensitivity, with the put benefiting from the underlying decline while theta and convexity play secondary roles. However, the attribution does not fully explain this move: a meaningful residual remains, so the story needs human review rather than a clean single-factor conclusion. With observation locked and no relevant headlines retrieved, there is no supported Layer B catalyst to add beyond the model revaluation.

### 2026-09-24/live_210022/legs/XOM.json

- **Off** (flags it): The model move is explained primarily by delta exposure: the put lost value as the underlying drifted higher, with the other Taylor buckets playing only secondary roles. Although implied volatility moved sharply, the observation lock and suppress flag mean this should not be turned into a Vega story, so the clean read is a spot-led revaluation with a small unexplained break that is consistent with path and truncation effects. The American exercise feature is not a meaningful contributor here, so the pricing change remains a standard engine revaluation rather than an exercise-boundary story.
- **On** (flags it): The position moved primarily with the underlying, so the desk attribution is dominated by delta. That said, the attribution does not explain this move cleanly: the terminal break flag means a meaningful part of the revaluation remains unexplained and needs human review. There are no retrieved headlines or named microstructure mechanisms here, so Layer B is empty and cannot be used to force a catalyst story.

### 2026-10-05/live_210138/legs/JPM.json

- **Off**: The move is primarily a delta-led revaluation: the put gained value as the underlying edged lower, with gamma only a minor helper and theta and implied volatility changes offsetting part of the gain. The run also shows a material model-versus-European gap from American exercise and dividend mechanics, so this is best read as a carry-and-exercise-aware pricing case rather than a clean single-factor move. No relevant headline catalyst was retrieved, so there is no separate news mechanism to assign.
- **On** (flags it): The Taylor pass points to delta as the main modeled driver, with the small spot decline providing the directional push and offsetting vega and theta. However, the attribution does not explain this move: the residual remains large enough that the story needs human review rather than a clean factor conclusion. With no relevant headlines retrieved, there is no Layer B catalyst to add, and the unresolved break should be treated as an unexplained model gap.

### 2026-10-05/live_210138/legs/META.json

- **Off**: The move is explained first by theta decay in the desk attribution, with delta and vega partly offsetting that erosion while gamma remained small. The full revaluation is essentially flat, and the remaining gap sits in the model residual rather than pointing to a separate named catalyst. Early exercise is not a factor here, so the American mark is behaving like the European cross-check.
- **On** (flags it): The modeled move is led by theta decay, with delta and vega also contributing while gamma stays minor. However, the attribution does not fully explain this move: a large unexplained break remains, so the story needs human review rather than a single-factor explanation.

### 2026-10-05/live_210138/legs/NVDA.json

- **Off**: The move is explained primarily by delta from the higher underlying print, with gamma adding a small convexity boost. Vega and theta offset much of that gain, leaving the revaluation effectively flat once the full engine is applied; the remaining break is best read as model- and path-related noise rather than a separate market catalyst.
- **On** (flags it): The attribution is led by spot-driven delta, with gamma a small positive offset and vega and theta acting as drags. However, the diagnostic does not fully explain the move: the residual is still material enough that this needs human review rather than a single-factor explanation.

### 2026-10-05/live_210138/legs/SPY.json

- **Off**: The move is dominated by the model’s vega bucket, with spot and gamma contributing only secondary offsetting effects. This is a full revaluation-style valuation shift inside the engine rather than a news-driven move, and the small residual is consistent with truncation and path effects around the option’s curvature and American features. No relevant headline catalyst was retrieved, so there is no separate Layer B mechanism to attribute beyond the model move itself.
- **On** (flags it): The dominant modeled driver is vega, with the position gaining on the implied-vol move while delta and theta partially offset that effect. However, the attribution does not explain this move cleanly: the residual is still material relative to the model change, so the story needs human review rather than a single-factor conclusion.

### 2026-10-05/live_210138/legs/TSLA.json

- **Off** (flags it): The move is explained first by the position’s positive delta responding to the higher underlying price, with gamma adding only a small convexity lift. That gain was partly offset by the drop in implied volatility and time decay, so the full revaluation was largely a spot-led move with a modest unexplained break in the model path. There is no TSLA-specific headline catalyst in the feed, so the news layer does not add a separate event story here.
- **On** (flags it): The modeled attribution is led by delta from the underlying move, with gamma a smaller convexity contributor and theta a modest drag. However, the attribution does not explain this move cleanly: the terminal break flag indicates a large unexplained gap that needs human review, so the Greek story should be treated as partial rather than definitive. The headline set adds no TSLA-specific catalyst or microstructure mechanism, so it does not supply the missing explanation.

### 2026-10-20/live_200122/legs/KO.json

- **Off**: The revaluation is primarily explained by the underlying drifting lower, with the option’s positive directional exposure doing most of the work. Theta decay also weighs on the mark, while the small residual is consistent with normal truncation rather than a separate event-driven gap. There is no retrieved catalyst tape here, so the move should be read as a clean model repricing rather than a headline-driven story.
- **On** (flags it): The dominant modeled driver is the spot-linked delta move, with theta also contributing meaningfully to the one-day revaluation. However, the attribution does not fully explain this move and the terminal-break flag means the story needs human review rather than a single clean catalyst call.

### 2026-10-23/live_200219/legs/KO.json

- **Off**: The move is explained primarily by the stock rally flowing through the call’s high delta, with a smaller convexity contribution and a positive vega tail from the higher implied volatility. The residual is small enough to fit normal higher-order truncation and pricing noise around the full revaluation. No headline catalyst was retrieved, so the tape reads as a model reprice on spot and volatility rather than a news-led event.
- **On** (flags it): The dominant modeled driver is the spot move flowing through delta, with gamma and vega adding smaller supporting effects. However, the attribution does not fully explain this move: the terminal break remains, so the story needs human review rather than a single-cause conclusion.

### 2026-10-26/live_210145/legs/KO.json

- **Off**: The option’s move was driven mainly by the drop in the underlying, with the Taylor breakdown showing delta as the clear dominant factor. Vega also helped pressure the model price because implied volatility fell, but the observation lock means there is no external catalyst layer to add beyond the blotter’s own market move. The small residual is consistent with ordinary higher-order effects rather than a separate event explanation.
- **On** (flags it): The modeled move is led by delta, with the lower underlying price driving most of the revaluation and a smaller contribution from implied volatility. However, the attribution does not fully explain this move: the diagnostic pass leaves a terminal unexplained break, so the story needs human review rather than a single-factor conclusion.

### 2026-10-27/live_210131/legs/KO.json

- **Off** (flags it): The position’s move was driven primarily by higher implied volatility in the model, with spot essentially flat and theta a small drag. Because the observation is flagged unreliable and the desk suppresses a Vega narrative, the residual should be treated as a model-side gap rather than a clean news attribution. The American vs European comparison also does not point to early exercise as the explanation; the dividend does not cover the remaining time value.
- **On** (flags it): The modeled move is led by a higher implied-volatility mark, with the option price rising as the vol input reset while spot was essentially unchanged. At the same time, the attribution does not fully explain this move: the terminal break leaves a meaningful remainder that needs human review rather than a single-factor conclusion. There are no retrieved headlines, so there is no confirmed external catalyst to add beyond the model revaluation.

### 2026-10-28/live_210145/legs/KO.json

- **Off**: The revaluation was driven primarily by the adverse spot move in the underlying, with the option’s directional exposure doing most of the work. Smaller offsetting contributions came from gamma, theta, and a modest implied-volatility decline, while the residual stayed low enough to look like ordinary Taylor truncation rather than a separate event. There are no retrieved headlines, so the tape here is a modeled spot-and-vol story rather than a news-driven catalyst case.
- **On** (flags it): The modeled move is led by delta, with the lower spot print doing most of the work and smaller contributions from implied volatility, theta, and gamma. That said, the attribution does not fully explain this move and the terminal-break flag means the story needs human review rather than a single-factor conclusion.
