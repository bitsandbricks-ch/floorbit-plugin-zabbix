"""The hosted part: keeps what the agent last sent and shows it on the dashboard."""
import time

from floorbit.plugins.base import Plugin as Base


class Plugin(Base):
    def agent_status(self, agent, payload):
        """What the agent part sent with ``ctx.send('status', ...)``, already checked against plugin.yaml."""
        up, total = int(payload.get('up') or 0), int(payload.get('total') or 0)
        self.ctx.set_state('status', {'up': up, 'total': total, 'agent': agent['name'], 'at': int(time.time())})
        return {'kept': True}

    def widget_summary(self):
        status = self.ctx.state.get('status')
        if not status:
            return {'type': 'stat', 'value': '-', 'sub': 'No word from the agent yet'}
        down = status['total'] - status['up']
        return {'type': 'stat', 'value': f"{status['up']} / {status['total']}", 'unit': 'up',
                'tone': 'ok' if not down else 'err' if not status['up'] else 'warn',
                'sub': f"from {status['agent']}"}
